import logging
import os
from pathlib import Path

import click

from zhixin import fs
from zhixin.package.exception import UnknownPackageError
from zhixin.package.manager.core import get_core_package_dir
from zhixin.package.manager.library import LibraryPackageManager
from zhixin.package.manager.platform import PlatformPackageManager
from zhixin.package.manager.tool import ToolPackageManager
from zhixin.package.meta import PackageCompatibility, PackageSpec
from zhixin.platform.exception import UnknownPlatform
from zhixin.platform.factory import PlatformFactory
from zhixin.project.config import ProjectConfig
from zhixin.project.savedeps import pkg_to_save_spec, save_project_dependencies
from zhixin.test.result import TestSuite
from zhixin.test.runners.factory import TestRunnerFactory


@click.command(
    "install", short_help="Install the project dependencies or custom packages"
)
@click.option(
    "-d",
    "--project-dir",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option("-e", "--environment", "environments", multiple=True)
@click.option("-p", "--platform", "platforms", metavar="SPECIFICATION", multiple=True)
@click.option("-t", "--tool", "tools", metavar="SPECIFICATION", multiple=True)
@click.option("-l", "--library", "libraries", metavar="SPECIFICATION", multiple=True)
@click.option(
    "--no-save",
    is_flag=True,
    help="Prevent saving specified packages to `zhixin.ini`",
)
@click.option("--skip-dependencies", is_flag=True, help="Skip package dependencies")
@click.option("-g", "--global", is_flag=True, help="Install package globally")
@click.option(
    "--storage-dir",
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Custom Package Manager storage for global packages",
)
@click.option("-f", "--force", is_flag=True, help="Reinstall package if it exists")
@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
def package_install_cmd(**options):
    if options.get("global") or options.get("storage_dir"):
        install_global_dependencies(options)
    else:
        install_project_dependencies(options)


def install_global_dependencies(options):
    pm = PlatformPackageManager(options.get("storage_dir"))
    tm = ToolPackageManager(options.get("storage_dir"))
    lm = LibraryPackageManager(options.get("storage_dir"))
    for obj in (pm, tm, lm):
        obj.set_log_level(logging.WARN if options.get("silent") else logging.DEBUG)
    for spec in options.get("platforms"):
        pm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )
    for spec in options.get("tools"):
        tm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )
    for spec in options.get("libraries", []):
        lm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )


def install_project_dependencies(options):
    environments = options["environments"]
    with fs.cd(options["project_dir"]):
        config = ProjectConfig.get_instance()
        config.validate(environments)
        for env in config.envs():
            if environments and env not in environments:
                continue
            if not options.get("silent"):
                click.echo("Resolving %s dependencies..." % click.style(env, fg="cyan"))
            already_up_to_date = not install_project_env_dependencies(env, options)
            if not options.get("silent") and already_up_to_date:
                click.secho("Already up-to-date.", fg="green")


def install_project_env_dependencies(project_env, options=None):
    """Used in `zx run` -> Processor"""
    options = options or {}
    installed_conds = []
    # custom platforms
    if options.get("platforms"):
        installed_conds.append(
            _install_project_env_custom_platforms(project_env, options)
        )
    # custom tools
    if options.get("tools"):
        installed_conds.append(_install_project_env_custom_tools(project_env, options))
    # custom libraries
    if options.get("libraries"):
        installed_conds.append(
            _install_project_env_custom_libraries(project_env, options)
        )
    # declared dependencies
    if not installed_conds:
        installed_conds = [
            _install_project_env_platform(project_env, options),
            _install_project_env_libraries(project_env, options),
        ]
    return any(installed_conds)


def _install_project_env_platform(project_env, options):
    config = ProjectConfig.get_instance()
    pm = PlatformPackageManager()
    if options.get("silent"):
        pm.set_log_level(logging.WARN)
    spec = config.get(f"env:{project_env}", "platform")
    if not spec:
        return False
    already_up_to_date = not options.get("force")
    if not pm.get_package(spec):
        already_up_to_date = False
    PlatformPackageManager().install(
        spec,
        project_env=project_env,
        project_targets=options.get("project_targets"),
        skip_dependencies=options.get("skip_dependencies"),
        force=options.get("force"),
    )
    # ensure SCons is installed
    get_core_package_dir("tool-scons")
    return not already_up_to_date


def _install_project_env_custom_platforms(project_env, options):
    already_up_to_date = not options.get("force")
    pm = PlatformPackageManager()
    if not options.get("silent"):
        pm.set_log_level(logging.DEBUG)
    for spec in options.get("platforms"):
        if not pm.get_package(spec):
            already_up_to_date = False
        pm.install(
            spec,
            project_env=project_env,
            project_targets=options.get("project_targets"),
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )
    return not already_up_to_date


def _install_project_env_custom_tools(project_env, options):
    already_up_to_date = not options.get("force")
    tm = ToolPackageManager()
    if not options.get("silent"):
        tm.set_log_level(logging.DEBUG)
    specs_to_save = []
    for tool in options.get("tools"):
        spec = PackageSpec(tool)
        if not tm.get_package(spec):
            already_up_to_date = False
        pkg = tm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )
        specs_to_save.append(pkg_to_save_spec(pkg, spec))
    if not options.get("no_save") and specs_to_save:
        save_project_dependencies(
            os.getcwd(),
            specs_to_save,
            scope="platform_packages",
            action="add",
            environments=[project_env],
        )
    return not already_up_to_date


def _install_project_env_libraries(project_env, options):
    _uninstall_project_unused_libdeps(project_env, options)
    already_up_to_date = not options.get("force")
    config = ProjectConfig.get_instance()

    compatibility_qualifiers = {}
    if config.get(f"env:{project_env}", "platform", None):
        try:
            p = PlatformFactory.new(config.get(f"env:{project_env}", "platform"))
            compatibility_qualifiers["platforms"] = [p.name]
        except UnknownPlatform:
            pass
        if config.get(f"env:{project_env}", "framework"):
            compatibility_qualifiers["frameworks"] = config.get(
                f"env:{project_env}", "framework"
            )

    env_lm = LibraryPackageManager(
        os.path.join(config.get("zhixin", "libdeps_dir"), project_env),
        compatibility=(
            PackageCompatibility(**compatibility_qualifiers)
            if compatibility_qualifiers
            else None
        ),
    )
    private_lm = LibraryPackageManager(
        os.path.join(config.get("zhixin", "lib_dir"))
    )
    if options.get("silent"):
        env_lm.set_log_level(logging.WARN)
        private_lm.set_log_level(logging.WARN)

    lib_deps = config.get(f"env:{project_env}", "lib_deps")
    if "__test" in options.get("project_targets", []):
        test_runner = TestRunnerFactory.new(
            TestSuite(project_env, options.get("zxtest_running_name", "*")), config
        )
        lib_deps.extend(test_runner.EXTRA_LIB_DEPS or [])

    for library in lib_deps:
        spec = PackageSpec(library)
        # skip built-in dependencies
        if not spec.external and not spec.owner:
            continue
        if not env_lm.get_package(spec):
            already_up_to_date = False
        env_lm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )

    # install dependencies from the private libraries
    for pkg in private_lm.get_installed():
        _install_project_private_library_deps(pkg, private_lm, env_lm, options)

    return not already_up_to_date


def _uninstall_project_unused_libdeps(project_env, options):
    config = ProjectConfig.get_instance()
    lib_deps = set(config.get(f"env:{project_env}", "lib_deps"))
    if not lib_deps:
        return
    storage_dir = Path(config.get("zhixin", "libdeps_dir"), project_env)
    integrity_dat = storage_dir / "integrity.dat"
    if integrity_dat.is_file():
        prev_lib_deps = set(
            integrity_dat.read_text(encoding="utf-8").strip().split("\n")
        )
        if lib_deps == prev_lib_deps:
            return
        lm = LibraryPackageManager(str(storage_dir))
        if options.get("silent"):
            lm.set_log_level(logging.WARN)
        else:
            click.secho("Removing unused dependencies...")
        for spec in set(prev_lib_deps) - set(lib_deps):
            try:
                lm.uninstall(spec)
            except UnknownPackageError:
                pass
    if not storage_dir.is_dir():
        storage_dir.mkdir(parents=True)
    integrity_dat.write_text("\n".join(lib_deps), encoding="utf-8")


def _install_project_private_library_deps(private_pkg, private_lm, env_lm, options):
    for dependency in private_lm.get_pkg_dependencies(private_pkg) or []:
        spec = private_lm.dependency_to_spec(dependency)
        # skip built-in dependencies
        if not spec.external and not spec.owner:
            continue
        pkg = private_lm.get_package(spec)
        if not pkg and not env_lm.get_package(spec):
            pkg = env_lm.install(
                spec,
                skip_dependencies=True,
                force=options.get("force"),
            )
        if not pkg:
            continue
        _install_project_private_library_deps(pkg, private_lm, env_lm, options)


def _install_project_env_custom_libraries(project_env, options):
    already_up_to_date = not options.get("force")
    config = ProjectConfig.get_instance()
    lm = LibraryPackageManager(
        os.path.join(config.get("zhixin", "libdeps_dir"), project_env)
    )
    if not options.get("silent"):
        lm.set_log_level(logging.DEBUG)
    specs_to_save = []
    for library in options.get("libraries") or []:
        spec = PackageSpec(library)
        if not lm.get_package(spec):
            already_up_to_date = False
        pkg = lm.install(
            spec,
            skip_dependencies=options.get("skip_dependencies"),
            force=options.get("force"),
        )
        specs_to_save.append(pkg_to_save_spec(pkg, spec))
    if not options.get("no_save") and specs_to_save:
        save_project_dependencies(
            os.getcwd(),
            specs_to_save,
            scope="lib_deps",
            action="add",
            environments=[project_env],
        )
    return not already_up_to_date
