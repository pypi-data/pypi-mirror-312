import json
import os
import re
import time
from glob import glob

from zhixin import __version__, exception, proc
from zhixin.compat import IS_MACOS, IS_WINDOWS


def list_serial_ports(filter_hwid=False, as_objects=False):
    try:
        # pylint: disable=import-outside-toplevel
        from serial.tools.list_ports import comports
    except ImportError as exc:
        raise exception.GetSerialPortsError(os.name) from exc

    if as_objects:
        return comports()

    result = []
    for p, d, h in comports():
        if not p:
            continue
        if not filter_hwid or "VID:PID" in h:
            result.append({"port": p, "description": d, "hwid": h})

    if filter_hwid:
        return result

    # fix for PySerial
    if not result and IS_MACOS:
        for p in glob("/dev/tty.*"):
            result.append({"port": p, "description": "n/a", "hwid": "n/a"})
    return result


def list_logical_devices():
    items = []
    if IS_WINDOWS:
        try:
            result = proc.exec_command(
                ["wmic", "logicaldisk", "get", "name,VolumeName"]
            ).get("out", "")
            devicenamere = re.compile(r"^([A-Z]{1}\:)\s*(\S+)?")
            for line in result.split("\n"):
                match = devicenamere.match(line.strip())
                if not match:
                    continue
                items.append({"path": match.group(1) + "\\", "name": match.group(2)})
            return items
        except WindowsError:  # pylint: disable=undefined-variable
            pass
        # try "fsutil"
        result = proc.exec_command(["fsutil", "fsinfo", "drives"]).get("out", "")
        for device in re.findall(r"[A-Z]:\\", result):
            items.append({"path": device, "name": None})
        return items

    result = proc.exec_command(["df"]).get("out")
    devicenamere = re.compile(r"^/.+\d+\%\s+([a-z\d\-_/]+)$", flags=re.I)
    for line in result.split("\n"):
        match = devicenamere.match(line.strip())
        if not match:
            continue
        items.append({"path": match.group(1), "name": os.path.basename(match.group(1))})
    return items


def list_mdns_services():
    try:
        import zeroconf  # pylint: disable=import-outside-toplevel
    except ImportError:
        result = proc.exec_command(
            [proc.get_pythonexe_path(), "-m", "pip", "install", "zeroconf"]
        )
        if result.get("returncode") != 0:
            print(result.get("err"))
        import zeroconf  # pylint: disable=import-outside-toplevel

    class mDNSListener:
        def __init__(self):
            self._zc = zeroconf.Zeroconf(interfaces=zeroconf.InterfaceChoice.All)
            self._found_types = []
            self._found_services = []

        def __enter__(self):
            zeroconf.ServiceBrowser(
                self._zc,
                [
                    "_http._tcp.local.",
                    "_hap._tcp.local.",
                    "_services._dns-sd._udp.local.",
                ],
                self,
            )
            return self

        def __exit__(self, etype, value, traceback):
            self._zc.close()

        def add_service(self, zc, type_, name):
            try:
                assert zeroconf.service_type_name(name)
                assert str(name)
            except (AssertionError, UnicodeError, zeroconf.BadTypeInNameException):
                return
            if name not in self._found_types:
                self._found_types.append(name)
                zeroconf.ServiceBrowser(self._zc, name, self)
            if type_ in self._found_types:
                s = zc.get_service_info(type_, name)
                if s:
                    self._found_services.append(s)

        def remove_service(self, zc, type_, name):
            pass

        def update_service(self, zc, type_, name):
            pass

        def get_services(self):
            return self._found_services

    items = []
    with mDNSListener() as mdns:
        time.sleep(3)
        for service in mdns.get_services():
            properties = None
            if service.properties:
                try:
                    properties = {
                        k.decode("utf8"): (
                            v.decode("utf8") if isinstance(v, bytes) else v
                        )
                        for k, v in service.properties.items()
                    }
                    json.dumps(properties)
                except UnicodeDecodeError:
                    properties = None

            items.append(
                {
                    "type": service.type,
                    "name": service.name,
                    "ip": ", ".join(service.parsed_addresses()),
                    "port": service.port,
                    "properties": properties,
                }
            )
    return items
