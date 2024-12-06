import json
import os

import click

from zhixin import fs
from zhixin.package.commands.install import install_project_dependencies
from zhixin.package.manager.platform import PlatformPackageManager
from zhixin.platform.exception import UnknownBoard
from zhixin.platform.factory import PlatformFactory
from zhixin.project.config import ProjectConfig
from zhixin.project.exception import UndefinedEnvPlatformError
from zhixin.project.helpers import is_zhixin_project
from zhixin.project.integration.generator import ProjectGenerator
from zhixin.project.options import ProjectOptions


def validate_boards(ctx, param, value):  # pylint: disable=unused-argument
    pm = PlatformPackageManager()
    for id_ in value:
        try:
            pm.board_config(id_)
        except UnknownBoard as exc:
            raise click.BadParameter(
                "`%s`. Please search for board ID using `zhixin boards` "
                "command" % id_
            ) from exc
    return value


@click.command("init", short_help="Initialize a project or update existing")
@click.option(
    "--project-dir",
    "-d",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "-b", "--board", "boards", multiple=True, metavar="ID", callback=validate_boards
)
@click.option("--ide", type=click.Choice(ProjectGenerator.get_supported_ides()))
@click.option("-e", "--environment", help="Update existing environment")
@click.option(
    "-O",
    "--project-option",
    "project_options",
    multiple=True,
    help="A `name=value` pair",
)
@click.option("--sample-code", is_flag=True)
@click.option("--no-install-dependencies", is_flag=True)
@click.option("--env-prefix", default="")
@click.option("-s", "--silent", is_flag=True)
def project_init_cmd(
    project_dir,
    boards,
    ide,
    environment,
    project_options,
    sample_code,
    no_install_dependencies,
    env_prefix,
    silent,
):
    project_dir = os.path.abspath(project_dir)
    is_new_project = not is_zhixin_project(project_dir)
    if is_new_project:
        if not silent:
            print_header(project_dir)
        init_base_project(project_dir)

    with fs.cd(project_dir):
        if environment:
            update_project_env(environment, project_options)
        elif boards:
            update_board_envs(project_dir, boards, project_options, env_prefix)
        else:
            update_project_comm(project_dir, ["name=%s" % os.path.basename(project_dir)])
                                        
        generator = None
        config = ProjectConfig.get_instance(os.path.join(project_dir, ".zxide", "zhixin.ini"))
        if ide:
            config.validate()
            # init generator and pick the best env if user didn't specify
            generator = ProjectGenerator(config, environment, ide, boards)
            if not environment:
                environment = generator.env_name

        # resolve project dependencies
        if not no_install_dependencies and (environment or boards):
            install_project_dependencies(
                options=dict(
                    project_dir=project_dir,
                    environments=[environment] if environment else [],
                    silent=silent,
                )
            )

        if environment and sample_code:
            init_sample_code(config, environment)

        # if generator:
        #     if not silent:
        #         click.echo(
        #             "Updating metadata for the %s IDE..." % click.style(ide, fg="cyan")
        #         )
        #     generator.generate()

        # if is_new_project:
        #     init_cvs_ignore()

    if not silent:
        print_footer(is_new_project)


def print_header(project_dir):
    click.echo("The following files/directories have been created in ", nl=False)
    try:
        click.secho(project_dir, fg="cyan")
    except UnicodeEncodeError:
        click.secho(json.dumps(project_dir), fg="cyan")
    click.echo("%s - Put project header files here" % click.style("include", fg="cyan"))
    # click.echo(
    #     "%s - Put project specific (private) libraries here"
    #     % click.style("lib", fg="cyan")
    # )
    click.echo("%s - Put project source files here" % click.style("src", fg="cyan"))
    click.echo(
        "%s - Project Configuration File" % click.style("zhixin.ini", fg="cyan")
    )


def print_footer(is_new_project):
    action = "initialized" if is_new_project else "updated"
    return click.secho(
        f"Project has been successfully {action}!",
        fg="green",
    )


def init_base_project(project_dir):
    with fs.cd(project_dir):
        config = ProjectConfig()
        config.save()
        dir_to_readme = [
            (config.get("zhixin", "src_dir"), None),
            (config.get("zhixin", "include_dir"), None),
            # (config.get("zhixin", "lib_dir"), init_lib_readme),
            # (config.get("zhixin", "test_dir"), init_test_readme),
        ]
        click.echo(dir_to_readme);
        for path, cb in dir_to_readme:
            if isinstance(path, list):
                click.echo(path[0]);
                if os.path.isdir(path[0]):
                    continue
                os.makedirs(path[0])
                if cb:
                    cb(path[0])
            else:
                click.echo(path);
                if os.path.isdir(path):
                    continue
                os.makedirs(path)
                if cb:
                    cb(path)


def init_include_readme(include_dir):
    with open(os.path.join(include_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project header files.

A header file is a file containing C declarations and macro definitions
to be shared between several project source files. You request the use of a
header file in your project source file (C, C++, etc) located in `src` folder
by including it, with the C preprocessing directive `#include'.

```src/main.c

#include "header.h"

int main (void)
{
 ...
}
```

Including a header file produces the same results as copying the header file
into each source file that needs it. Such copying would be time-consuming
and error-prone. With a header file, the related declarations appear
in only one place. If they need to be changed, they can be changed in one
place, and programs that include the header file will automatically use the
new version when next recompiled. The header file eliminates the labor of
finding and changing all the copies as well as the risk that a failure to
find one copy will result in inconsistencies within a program.

In C, the usual convention is to give header files names that end with `.h'.
It is most portable to use only letters, digits, dashes, and underscores in
header file names, and at most one dot.

Read more about using header files in official GCC documentation:

* Include Syntax
* Include Operation
* Once-Only Headers
* Computed Includes

https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html
""",
        )


# def init_lib_readme(lib_dir):
#     with open(os.path.join(lib_dir, "README"), mode="w", encoding="utf8") as fp:
#         fp.write()


# def init_test_readme(test_dir):
#     with open(os.path.join(test_dir, "README"), mode="w", encoding="utf8") as fp:
#         fp.write()


def init_cvs_ignore():
    conf_path = ".gitignore"
    if os.path.isfile(conf_path):
        return
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(".zx\n")


def update_board_envs(project_dir, boards, extra_project_options, env_prefix):
    config = ProjectConfig(
        os.path.join(project_dir, ".zxide", "zhixin.ini"), parse_extra=False
    )
    used_boards = []
    for section in config.sections():
        cond = [section.startswith("env:"), config.has_option(section, "board")]
        if all(cond):
            used_boards.append(config.get(section, "board"))

    pm = PlatformPackageManager()
    modified = False
    for id_ in boards:
        board_config = pm.board_config(id_)
        if id_ in used_boards:
            continue
        used_boards.append(id_)
        modified = True

        envopts = {"platform": board_config["platform"], "board": id_}
        # find default framework for board
        frameworks = board_config.get("frameworks")
        if frameworks:
            envopts["framework"] = frameworks[0]

        for item in extra_project_options:
            if "=" not in item:
                continue
            _name, _value = item.split("=", 1)
            envopts[_name.strip()] = _value.strip()

        section = "env:%s%s" % (env_prefix, id_)
        config.add_section(section)

        for option, value in envopts.items():
            config.set(section, option, value)

    if modified:
        config.save()


def update_project_env(environment, extra_project_options=None):
    if not extra_project_options:
        return
    env_section = "env:%s" % environment
    option_to_sections = {"zhixin": [], env_section: []}
    for item in extra_project_options:
        assert "=" in item
        name, value = item.split("=", 1)
        name = name.strip()
        destination = env_section
        for option in ProjectOptions.values():
            if option.scope in option_to_sections and option.name == name:
                destination = option.scope
                break
        option_to_sections[destination].append((name, value.strip()))

    config = ProjectConfig(
        "zhixin.ini", parse_extra=False, expand_interpolations=False
    )
    for section, options in option_to_sections.items():
        if not options:
            continue
        if not config.has_section(section):
            config.add_section(section)
        for name, value in options:
            config.set(section, name, value)

    config.save()

def update_project_comm(project_dir, extra_project_options=None):
    if not extra_project_options:
        return
    option_to_sections = {"zhixin": []}
    for item in extra_project_options:
        assert "=" in item
        name, value = item.split("=", 1)
        name = name.strip()
        destination = "zhixin"
        for option in ProjectOptions.values():
            if option.scope in option_to_sections and option.name == name:
                destination = option.scope
                break
        option_to_sections[destination].append((name, value.strip()))

    config = ProjectConfig(
        os.path.join(project_dir, ".zxide", "zhixin.ini"), parse_extra=False, expand_interpolations=False
    )

    for section, options in option_to_sections.items():
        if not options:
            continue
        if not config.has_section(section):
            config.add_section(section)
        for name, value in options:
            config.set(section, name, value)

    config.save()

def init_sample_code(config, environment):
    try:
        p = PlatformFactory.from_env(environment)
        return p.generate_sample_code(config, environment)
    except (NotImplementedError, UndefinedEnvPlatformError):
        pass

    framework = config.get(f"env:{environment}", "framework", None)
    if framework != ["arduino"]:
        return None
    main_content = """"""
    is_cpp_project = p.name not in ["intel_mcs51", "ststm8"]
    src_dir = config.get("zhixin", "src_dir")
    main_path = os.path.join(src_dir, "main.%s" % ("cpp" if is_cpp_project else "c"))
    if os.path.isfile(main_path):
        return None
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    with open(main_path, mode="w", encoding="utf8") as fp:
        fp.write(main_content.strip())
    return True
