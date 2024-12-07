import os
import re
import subprocess
from enum import Enum

import click

from zhixin.compat import IS_MACOS


class ShellType(Enum):
    FISH = "fish"
    ZSH = "zsh"
    BASH = "bash"


def get_bash_version():
    output = subprocess.run(
        ["bash", "--version"], check=True, stdout=subprocess.PIPE
    ).stdout.decode()
    match = re.search(r"version\s+(\d+)\.(\d+)", output, re.IGNORECASE)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (0, 0)


def get_completion_install_path(shell):
    home_dir = os.path.expanduser("~")
    prog_name = click.get_current_context().find_root().info_name
    if shell == ShellType.FISH:
        return os.path.join(
            home_dir, ".config", "fish", "completions", "%s.fish" % prog_name
        )
    if shell == ShellType.ZSH:
        return os.path.join(home_dir, ".zshrc")
    if shell == ShellType.BASH:
        return os.path.join(home_dir, ".bash_completion")
    raise click.ClickException("%s is not supported." % shell)


def get_completion_code(shell):
    if shell == ShellType.FISH:
        return "eval (env _ZX_COMPLETE=fish_source zx)"
    if shell == ShellType.ZSH:
        code = "autoload -Uz compinit\ncompinit\n" if IS_MACOS else ""
        return code + 'eval "$(_ZX_COMPLETE=zsh_source zx)"'
    if shell == ShellType.BASH:
        return 'eval "$(_ZX_COMPLETE=bash_source zx)"'
    raise click.ClickException("%s is not supported." % shell)


def is_completion_code_installed(shell, path):
    if shell == ShellType.FISH or not os.path.exists(path):
        return False
    with open(path, encoding="utf8") as fp:
        return get_completion_code(shell) in fp.read()


def install_completion_code(shell, path):
    if shell == ShellType.BASH and get_bash_version() < (4, 4):
        raise click.ClickException("The minimal supported Bash version is 4.4")
    if is_completion_code_installed(shell, path):
        return None
    append = shell != ShellType.FISH
    with open(path, mode="a" if append else "w", encoding="utf8") as fp:
        if append:
            fp.write("\n\n# Begin: ZhiXin Core completion support\n")
        fp.write(get_completion_code(shell))
        if append:
            fp.write("\n# End: ZhiXin Core completion support\n\n")
    return True


def uninstall_completion_code(shell, path):
    if not os.path.exists(path):
        return True
    if shell == ShellType.FISH:
        os.remove(path)
        return True

    with open(path, "r+", encoding="utf8") as fp:
        contents = fp.read()
        fp.seek(0)
        fp.truncate()
        fp.write(contents.replace(get_completion_code(shell), ""))

    return True
