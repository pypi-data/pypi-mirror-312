from datetime import datetime
from time import time

import click
from twisted.internet import defer, endpoints, reactor  # pylint: disable=import-error
from twisted.logger import ILogObserver  # pylint: disable=import-error
from twisted.logger import Logger  # pylint: disable=import-error
from twisted.logger import LogLevel  # pylint: disable=import-error
from twisted.logger import formatEvent  # pylint: disable=import-error
from twisted.python import failure  # pylint: disable=import-error
from twisted.spread import pb  # pylint: disable=import-error
from zope.interface import provider  # pylint: disable=import-error

from zhixin import __zxremote_endpoint__, __version__, app, exception, maintenance
from zhixin.remote.factory.client import RemoteClientFactory
from zhixin.remote.factory.ssl import SSLContextFactory


class RemoteClientBase(  # pylint: disable=too-many-instance-attributes
    pb.Referenceable
):
    PING_DELAY = 60
    PING_MAX_FAILURES = 3
    DEBUG = False

    def __init__(self):
        self.log_level = LogLevel.warn
        self.log = Logger(namespace="remote", observer=self._log_observer)
        self.id = app.get_host_id()
        self.name = app.get_host_name()
        self.join_options = {"corever": __version__}
        self.perspective = None
        self.agentpool = None

        self._ping_id = 0
        self._ping_caller = None
        self._ping_counter = 0
        self._reactor_stopped = False
        self._exit_code = 0

    @provider(ILogObserver)
    def _log_observer(self, event):
        if not self.DEBUG and (
            event["log_namespace"] != self.log.namespace
            or self.log_level > event["log_level"]
        ):
            return
        msg = formatEvent(event)
        click.echo(
            "%s [%s] %s"
            % (
                datetime.fromtimestamp(event["log_time"]).strftime("%Y-%m-%d %H:%M:%S"),
                event["log_level"].name,
                msg,
            )
        )

    def connect(self):
        self.log.info("Name: {name}", name=self.name)
        self.log.info("Connecting to ZhiXin Remote Development Cloud")

        # pylint: disable=protected-access
        proto, options = endpoints._parse(__zxremote_endpoint__)
        proto = proto[0]

        factory = RemoteClientFactory()
        factory.remote_client = self
        factory.sslContextFactory = None
        if proto == "ssl":
            factory.sslContextFactory = SSLContextFactory(options["host"])
            reactor.connectSSL(
                options["host"],
                int(options["port"]),
                factory,
                factory.sslContextFactory,
            )
        elif proto == "tcp":
            reactor.connectTCP(options["host"], int(options["port"]), factory)
        else:
            raise exception.ZhixinException("Unknown ZX Remote Cloud protocol")
        reactor.run()

        if self._exit_code != 0:
            raise exception.ReturnErrorCode(self._exit_code)

    def cb_client_authorization_failed(self, err):
        msg = "Bad account credentials"
        if err.check(pb.Error):
            msg = err.getErrorMessage()
        self.log.error(msg)
        self.disconnect(exit_code=1)

    def cb_client_authorization_made(self, perspective):
        self.log.info("Successfully authorized")
        self.perspective = perspective
        d = perspective.callRemote("join", self.id, self.name, self.join_options)
        d.addCallback(self._cb_client_join_made)
        d.addErrback(self.cb_global_error)

    def _cb_client_join_made(self, result):
        code = result[0]
        if code == 1:
            self.agentpool = result[1]
            self.agent_pool_ready()
            self.restart_ping()
        elif code == 2:
            self.remote_service(*result[1:])

    def remote_service(self, command, options):
        if command == "disconnect":
            self.log.error(
                "ZX Remote Cloud disconnected: {msg}", msg=options.get("message")
            )
            self.disconnect()

    def restart_ping(self, reset_counter=True):
        # stop previous ping callers
        self.stop_ping(reset_counter)
        self._ping_caller = reactor.callLater(self.PING_DELAY, self._do_ping)

    def _do_ping(self):
        self._ping_counter += 1
        self._ping_id = int(time())
        d = self.perspective.callRemote("service", "ping", {"id": self._ping_id})
        d.addCallback(self._cb_pong)
        d.addErrback(self._cb_pong)

    def stop_ping(self, reset_counter=True):
        if reset_counter:
            self._ping_counter = 0
        if not self._ping_caller or not self._ping_caller.active():
            return
        self._ping_caller.cancel()
        self._ping_caller = None

    def _cb_pong(self, result):
        if not isinstance(result, failure.Failure) and self._ping_id == result:
            self.restart_ping()
            return
        if self._ping_counter >= self.PING_MAX_FAILURES:
            self.stop_ping()
            self.perspective.broker.transport.loseConnection()
        else:
            self.restart_ping(reset_counter=False)

    def agent_pool_ready(self):
        raise NotImplementedError

    def disconnect(self, exit_code=None):
        self.stop_ping()
        if exit_code is not None:
            self._exit_code = exit_code
        if reactor.running and not self._reactor_stopped:
            self._reactor_stopped = True
            reactor.stop()

    def cb_disconnected(self, _):
        self.stop_ping()
        self.perspective = None
        self.agentpool = None

    def cb_global_error(self, err):
        if err.check(pb.PBConnectionLost, defer.CancelledError):
            return

        msg = err.getErrorMessage()
        if err.check(pb.DeadReferenceError):
            msg = "Remote Client has been terminated"
        elif "ZxAgentNotStartedError" in str(err.type):
            msg = (
                "Could not find active agents. Please start it before on "
                "a remote machine using `zx remote agent start` command.\n"
                "See http://docs.ZhiXin-Semi.com/page/plus/zx-remote.html"
            )
        else:
            maintenance.on_zhixin_exception(Exception(err.type))
        click.secho(msg, fg="red", err=True)
        self.disconnect(exit_code=1)
