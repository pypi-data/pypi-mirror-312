import asyncio
import functools
import io
import json
import os
import sys
import threading

import click
from ajsonrpc.core import JSONRPC20DispatchException

from zhixin import __main__, __version__, app, fs, proc, util
from zhixin.compat import (
    IS_WINDOWS,
    aio_create_task,
    aio_get_running_loop,
    aio_to_thread,
    get_locale_encoding,
    is_bytes,
)
from zhixin.exception import ZhixinException
from zhixin.home.rpc.handlers.base import BaseRPCHandler


class ZXCoreProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future, on_data_callback=None):
        self.exit_future = exit_future
        self.on_data_callback = on_data_callback
        self.stdout = ""
        self.stderr = ""
        self._is_exited = False
        self._encoding = get_locale_encoding()

    def pipe_data_received(self, fd, data):
        data = data.decode(self._encoding, "replace")
        pipe = ["stdin", "stdout", "stderr"][fd]
        if pipe == "stdout":
            self.stdout += data
        if pipe == "stderr":
            self.stderr += data
        if self.on_data_callback:
            self.on_data_callback(pipe=pipe, data=data)

    def connection_lost(self, exc):
        self.process_exited()

    def process_exited(self):
        if self._is_exited:
            return
        self.exit_future.set_result(True)
        self._is_exited = True


class MultiThreadingStdStream:
    def __init__(self, parent_stream):
        self._buffers = {threading.get_ident(): parent_stream}

    def __getattr__(self, name):
        thread_id = threading.get_ident()
        self._ensure_thread_buffer(thread_id)
        return getattr(self._buffers[thread_id], name)

    def _ensure_thread_buffer(self, thread_id):
        if thread_id not in self._buffers:
            self._buffers[thread_id] = io.StringIO()

    def write(self, value):
        thread_id = threading.get_ident()
        self._ensure_thread_buffer(thread_id)
        return self._buffers[thread_id].write(
            value.decode() if is_bytes(value) else value
        )

    def get_value_and_reset(self):
        result = ""
        try:
            result = self.getvalue()
            self.seek(0)
            self.truncate(0)
        except AttributeError:
            pass
        return result


@util.memoized(expire="60s")
def get_core_fullpath():
    return proc.where_is_program("zhixin" + (".exe" if IS_WINDOWS else ""))


class ZXCoreRPC(BaseRPCHandler):
    @staticmethod
    def version():
        return __version__

    async def exec(self, args, options=None):
        loop = aio_get_running_loop()
        exit_future = loop.create_future()
        data_callback = functools.partial(
            self._on_exec_data_received, exec_options=options
        )
        if args[0] != "--caller" and app.get_session_var("caller_id"):
            args = ["--caller", app.get_session_var("caller_id")] + args
        transport, protocol = await loop.subprocess_exec(
            lambda: ZXCoreProtocol(exit_future, data_callback),
            get_core_fullpath(),
            *args,
            stdin=None,
            **options.get("spawn", {}),
        )
        await exit_future
        transport.close()
        return {
            "stdout": protocol.stdout,
            "stderr": protocol.stderr,
            "returncode": transport.get_returncode(),
        }

    def _on_exec_data_received(self, exec_options, pipe, data):
        notification_method = exec_options.get(f"{pipe}NotificationMethod")
        if not notification_method:
            return
        aio_create_task(
            self.factory.notify_clients(
                method=notification_method,
                params=[data],
                actor="frontend",
            )
        )

    @staticmethod
    def setup_multithreading_std_streams():
        if isinstance(sys.stdout, MultiThreadingStdStream):
            return
        ZXCoreRPC.thread_stdout = MultiThreadingStdStream(sys.stdout)
        ZXCoreRPC.thread_stderr = MultiThreadingStdStream(sys.stderr)
        sys.stdout = ZXCoreRPC.thread_stdout
        sys.stderr = ZXCoreRPC.thread_stderr

    @staticmethod
    async def call(args, options=None):
        for i, arg in enumerate(args):
            if not isinstance(arg, str):
                args[i] = str(arg)

        options = options or {}
        to_json = "--json-output" in args

        try:
            if options.get("force_subprocess"):
                result = await ZXCoreRPC._call_subprocess(args, options)
                return ZXCoreRPC._process_result(result, to_json)
            result = await ZXCoreRPC._call_inline(args, options)
            try:
                return ZXCoreRPC._process_result(result, to_json)
            except ValueError:
                # fall-back to subprocess method
                result = await ZXCoreRPC._call_subprocess(args, options)
                return ZXCoreRPC._process_result(result, to_json)
        except Exception as exc:  # pylint: disable=bare-except
            raise JSONRPC20DispatchException(
                code=5000, message="ZX Core Call Error", data=str(exc)
            ) from exc

    @staticmethod
    async def _call_subprocess(args, options):
        result = await aio_to_thread(
            proc.exec_command,
            [get_core_fullpath()] + args,
            cwd=options.get("cwd") or os.getcwd(),
        )
        return (result["out"], result["err"], result["returncode"])

    @staticmethod
    async def _call_inline(args, options):
        ZXCoreRPC.setup_multithreading_std_streams()

        def _thread_safe_call(args, cwd):
            with fs.cd(cwd):
                exit_code = __main__.main(["-c"] + args)
            return (
                ZXCoreRPC.thread_stdout.get_value_and_reset(),
                ZXCoreRPC.thread_stderr.get_value_and_reset(),
                exit_code,
            )

        return await aio_to_thread(
            _thread_safe_call, args=args, cwd=options.get("cwd") or os.getcwd()
        )

    @staticmethod
    def _process_result(result, to_json=False):
        out, err, code = result
        if out and is_bytes(out):
            out = out.decode(get_locale_encoding())
        if err and is_bytes(err):
            err = err.decode(get_locale_encoding())
        text = ("%s\n\n%s" % (out, err)).strip()
        if code != 0:
            raise ZhixinException(text)
        if not to_json:
            return text
        try:
            return json.loads(out)
        except ValueError as exc:
            click.secho("%s => `%s`" % (exc, out), fg="red", err=True)
            # if ZX Core prints unhandled warnings
            for line in out.split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    return json.loads(line)
                except ValueError:
                    pass
            raise exc
