import signal
import sys
import threading

import click
import serial
from serial.tools import miniterm

from zhixin.exception import UserSideException


class Terminal(miniterm.Miniterm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zx_unexpected_exception = None

    def reader(self):
        try:
            super().reader()
        except Exception as exc:  # pylint: disable=broad-except
            self.zx_unexpected_exception = exc

    def writer(self):
        try:
            super().writer()
        except Exception as exc:  # pylint: disable=broad-except
            self.zx_unexpected_exception = exc


def get_available_filters():
    return sorted(miniterm.TRANSFORMATIONS.keys())


def start_terminal(options):
    retries = 0
    is_port_valid = False
    while True:
        term = None
        try:
            term = new_terminal(options)
            is_port_valid = True
            options["port"] = term.serial.name
            if retries:
                click.echo("\t Connected!", err=True)
            elif not options["quiet"]:
                print_terminal_settings(term)
            retries = 0  # reset
            term.start()
            try:
                term.join(True)
            except KeyboardInterrupt:
                pass
            term.join()

            # cleanup
            term.console.cleanup()

            # restore original standard streams
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            term.close()

            if term.zx_unexpected_exception:
                click.secho(
                    "Disconnected (%s)" % term.zx_unexpected_exception,
                    fg="red",
                    err=True,
                )
                if not options["no_reconnect"]:
                    raise UserSideException(term.zx_unexpected_exception)

            return
        except UserSideException as exc:
            if not is_port_valid:
                raise exc
            if not retries:
                click.echo("Reconnecting to %s " % options["port"], err=True, nl=False)
                signal.signal(signal.SIGINT, signal.SIG_DFL)
            else:
                click.echo(".", err=True, nl=False)
            retries += 1
            threading.Event().wait(retries / 2)


def new_terminal(options):
    term = Terminal(
        new_serial_instance(options),
        echo=options["echo"],
        eol=options["eol"].lower(),
        filters=list(reversed(options["filters"] or ["default"])),
    )
    term.exit_character = chr(options["exit_char"])
    term.menu_character = chr(options["menu_char"])
    term.raw = options["raw"]
    term.set_rx_encoding(options["encoding"])
    term.set_tx_encoding(options["encoding"])
    for ts in (term.tx_transformations, term.rx_transformations):
        for t in ts:
            try:
                t.set_running_terminal(term)
            except AttributeError:
                pass
    return term


def print_terminal_settings(terminal):
    click.echo(
        "--- Terminal on {p.name} | "
        "{p.baudrate} {p.bytesize}-{p.parity}-{p.stopbits}".format(p=terminal.serial)
    )
    click.echo(
        "--- Available filters and text transformations: %s"
        % ", ".join(get_available_filters())
    )
    click.echo("--- More details at https://bit.ly/zx-monitor-filters")
    click.echo(
        "--- Quit: {} | Menu: {} | Help: {} followed by {}".format(
            miniterm.key_description(terminal.exit_character),
            miniterm.key_description(terminal.menu_character),
            miniterm.key_description(terminal.menu_character),
            miniterm.key_description("\x08"),
        )
    )


def new_serial_instance(options):  # pylint: disable=too-many-branches
    serial_instance = None
    port = options["port"]
    while serial_instance is None:
        # no port given on command line -> ask user now
        if port is None or port == "-":
            try:
                port = miniterm.ask_for_port()
            except KeyboardInterrupt as exc:
                click.echo("", err=True)
                raise UserSideException("User aborted and port is not given") from exc
            if not port:
                raise UserSideException("Port is not given")
        try:
            serial_instance = serial.serial_for_url(
                port,
                options["baud"],
                parity=options["parity"],
                rtscts=options["rtscts"],
                xonxoff=options["xonxoff"],
                do_not_open=True,
            )

            if not hasattr(serial_instance, "cancel_read"):
                # enable timeout for alive flag polling if cancel_read is not available
                serial_instance.timeout = 1

            if options["dtr"] is not None:
                if not options["quiet"]:
                    click.echo(
                        "--- forcing DTR {}".format(
                            "active" if options["dtr"] else "inactive"
                        )
                    )
                serial_instance.dtr = options["dtr"]

            if options["rts"] is not None:
                if not options["quiet"]:
                    click.echo(
                        "--- forcing RTS {}".format(
                            "active" if options["rts"] else "inactive"
                        )
                    )
                serial_instance.rts = options["rts"]

            if isinstance(serial_instance, serial.Serial):
                serial_instance.exclusive = True

            serial_instance.open()
        except serial.SerialException as exc:
            raise UserSideException(exc) from exc

    return serial_instance
