import json
import platform
import sys

import click
from tabulate import tabulate

from zhixin import __version__, compat, proc, util
from zhixin.package.manager.library import LibraryPackageManager
from zhixin.package.manager.platform import PlatformPackageManager
from zhixin.package.manager.tool import ToolPackageManager
from zhixin.project.config import ProjectConfig


@click.command("info", short_help="Display system-wide information")
@click.option("--json-output", is_flag=True)
def system_info_cmd(json_output):
    project_config = ProjectConfig()
    data = {}
    data["core_version"] = {"title": "ZhiXin Core", "value": __version__}
    data["python_version"] = {
        "title": "Python",
        "value": "{0}.{1}.{2}-{3}.{4}".format(*list(sys.version_info)),
    }
    data["system"] = {"title": "System Type", "value": util.get_systype()}
    data["platform"] = {"title": "Platform", "value": platform.platform(terse=True)}
    data["filesystem_encoding"] = {
        "title": "File System Encoding",
        "value": compat.get_filesystem_encoding(),
    }
    data["locale_encoding"] = {
        "title": "Locale Encoding",
        "value": compat.get_locale_encoding(),
    }
    data["core_dir"] = {
        "title": "ZhiXin Core Directory",
        "value": project_config.get("zhixin", "core_dir"),
    }
    data["zhixin_exe"] = {
        "title": "ZhiXin Core Executable",
        "value": proc.where_is_program(
            "zhixin.exe" if compat.IS_WINDOWS else "zhixin"
        ),
    }
    data["python_exe"] = {
        "title": "Python Executable",
        "value": proc.get_pythonexe_path(),
    }
    data["global_lib_nums"] = {
        "title": "Global Libraries",
        "value": len(LibraryPackageManager().get_installed()),
    }
    data["dev_platform_nums"] = {
        "title": "Development Platforms",
        "value": len(PlatformPackageManager().get_installed()),
    }
    data["package_tool_nums"] = {
        "title": "Tools & Toolchains",
        "value": len(
            ToolPackageManager(
                project_config.get("zhixin", "packages_dir")
            ).get_installed()
        ),
    }
    click.echo(
        json.dumps(data)
        if json_output
        else tabulate([(item["title"], item["value"]) for item in data.values()])
    )
