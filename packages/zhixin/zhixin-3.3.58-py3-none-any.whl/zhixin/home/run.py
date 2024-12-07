import os
from urllib.parse import urlparse

import click
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_403_FORBIDDEN

from zhixin.compat import aio_get_running_loop
from zhixin.exception import ZhixinException
from zhixin.home.rpc.handlers.account import AccountRPC
from zhixin.home.rpc.handlers.app import AppRPC
from zhixin.home.rpc.handlers.ide import IDERPC
from zhixin.home.rpc.handlers.misc import MiscRPC
from zhixin.home.rpc.handlers.os import OSRPC
from zhixin.home.rpc.handlers.zxcore import ZXCoreRPC
from zhixin.home.rpc.handlers.platform import PlatformRPC
from zhixin.home.rpc.handlers.project import ProjectRPC
from zhixin.home.rpc.handlers.registry import RegistryRPC
from zhixin.home.rpc.server import WebSocketJSONRPCServerFactory
from zhixin.package.manager.core import get_core_package_dir
from zhixin.proc import force_exit


class ShutdownMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and b"__shutdown__" in scope.get("query_string", ""):
            await shutdown_server()
        await self.app(scope, receive, send)


async def shutdown_server(_=None):
    aio_get_running_loop().call_later(0.5, force_exit)
    return PlainTextResponse("Server has been shutdown!")


async def protected_page(_):
    return PlainTextResponse(
        "Protected ZhiXin Home session", status_code=HTTP_403_FORBIDDEN
    )


def run_server(host, port, no_open, shutdown_timeout, home_url):
    contrib_dir = get_core_package_dir("contrib-zxhome")
    if not os.path.isdir(contrib_dir):
        raise ZhixinException("Invalid path to ZX Home Contrib")

    ws_rpc_factory = WebSocketJSONRPCServerFactory(shutdown_timeout)
    ws_rpc_factory.add_object_handler(AccountRPC(), namespace="account")
    ws_rpc_factory.add_object_handler(AppRPC(), namespace="app")
    ws_rpc_factory.add_object_handler(IDERPC(), namespace="ide")
    ws_rpc_factory.add_object_handler(MiscRPC(), namespace="misc")
    ws_rpc_factory.add_object_handler(OSRPC(), namespace="os")
    ws_rpc_factory.add_object_handler(ZXCoreRPC(), namespace="core")
    ws_rpc_factory.add_object_handler(ProjectRPC(), namespace="project")
    ws_rpc_factory.add_object_handler(PlatformRPC(), namespace="platform")
    ws_rpc_factory.add_object_handler(RegistryRPC(), namespace="registry")

    path = urlparse(home_url).path
    routes = [
        WebSocketRoute(path + "wsrpc", ws_rpc_factory, name="wsrpc"),
        Route(path + "__shutdown__", shutdown_server, methods=["POST"]),
        Mount(path, StaticFiles(directory=contrib_dir, html=True), name="static"),
    ]
    if path != "/":
        routes.append(Route("/", protected_page))

    uvicorn.run(
        Starlette(
            middleware=[Middleware(ShutdownMiddleware)],
            routes=routes,
            on_startup=[
                lambda: click.echo(
                    "ZX Home has been started. Press Ctrl+C to shutdown."
                ),
                lambda: None if no_open else click.launch(home_url),
            ],
        ),
        host=host,
        port=port,
        log_level="warning",
    )
