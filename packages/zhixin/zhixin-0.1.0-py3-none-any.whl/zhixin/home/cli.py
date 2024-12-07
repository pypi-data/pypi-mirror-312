import mimetypes
import socket

import click

from zhixin.compat import IS_WINDOWS
from zhixin.home.run import run_server
from zhixin.package.manager.core import get_core_package_dir


@click.command("home", short_help="GUI to manage ZhiXin")
@click.option("--port", type=int, default=8008, help="HTTP port, default=8008")
@click.option(
    "--host",
    default="127.0.0.1",
    help=(
        "HTTP host, default=127.0.0.1. You can open ZX Home for inbound "
        "connections with --host=0.0.0.0"
    ),
)
@click.option("--no-open", is_flag=True)
@click.option(
    "--shutdown-timeout",
    default=0,
    type=int,
    help=(
        "Automatically shutdown server on timeout (in seconds) when no clients "
        "are connected. Default is 0 which means never auto shutdown"
    ),
)
@click.option(
    "--session-id",
    help=(
        "A unique session identifier to keep ZX Home isolated from other instances "
        "and protect from 3rd party access"
    ),
)
def cli(port, host, no_open, shutdown_timeout, session_id):
    # hook for `zhixin-node-helpers`
    if host == "__do_not_start__":
        # download all dependent packages
        get_core_package_dir("contrib-zxhome")
        return

    # Ensure ZX Home mimetypes are known
    mimetypes.add_type("text/html", ".html")
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("application/javascript", ".js")

    home_url = "http://%s:%d%s" % (
        host,
        port,
        ("/session/%s/" % session_id) if session_id else "/",
    )
    click.echo(
        "\n".join(
            [
                "",
                "  ___I_",
                " /\\-_--\\   ZhiXin Home",
                "/  \\_-__\\",
                "|[]| [] |  %s" % home_url,
                "|__|____|__%s" % ("_" * len(home_url)),
            ]
        )
    )
    click.echo("")
    click.echo("Open ZhiXin Home in your browser by this URL => %s" % home_url)

    if is_port_used(host, port):
        click.secho(
            "ZhiXin Home server is already started in another process.", fg="yellow"
        )
        if not no_open:
            click.launch(home_url)
        return

    run_server(
        host=host,
        port=port,
        no_open=no_open,
        shutdown_timeout=shutdown_timeout,
        home_url=home_url,
    )


def is_port_used(host, port):
    socket.setdefaulttimeout(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if IS_WINDOWS:
        try:
            s.bind((host, port))
            s.close()
            return False
        except (OSError, socket.error):
            pass
    else:
        try:
            s.connect((host, port))
            s.close()
        except socket.error:
            return False

    return True
