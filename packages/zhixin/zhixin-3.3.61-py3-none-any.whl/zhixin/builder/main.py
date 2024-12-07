import json
import os
import sys
from time import time

import click
from SCons.Script import ARGUMENTS  # pylint: disable=import-error
from SCons.Script import COMMAND_LINE_TARGETS  # pylint: disable=import-error
from SCons.Script import DEFAULT_TARGETS  # pylint: disable=import-error
from SCons.Script import AllowSubstExceptions  # pylint: disable=import-error
from SCons.Script import AlwaysBuild  # pylint: disable=import-error
from SCons.Script import Default  # pylint: disable=import-error
from SCons.Script import DefaultEnvironment  # pylint: disable=import-error
from SCons.Script import Import  # pylint: disable=import-error
from SCons.Script import Variables  # pylint: disable=import-error

from zhixin import app, fs
from zhixin.platform.base import PlatformBase
from zhixin.proc import get_pythonexe_path
from zhixin.project.helpers import get_project_dir

AllowSubstExceptions(NameError)

# append CLI arguments to build environment
clivars = Variables(None)
clivars.AddVariables(
    ("BUILD_SCRIPT",),
    ("PROJECT_CONFIG",),
    ("ZXENV",),
    ("ZXTEST_RUNNING_NAME",),
    ("UPLOAD_PORT",),
    ("PROGRAM_ARGS",),
)

DEFAULT_ENV_OPTIONS = dict(
    tools=[
        "ar",
        "cc",
        "c++",
        "link",
        "zxhooks",
        "zxasm",
        "zxbuild",
        "zxproject",
        "zxplatform",
        "zxtest",
        "zxtarget",
        "zxlib",
        "zxupload",
        "zxsize",
        "zxino",
        "zxmisc",
        "zxintegration",
        "zxmaxlen",
    ],
    toolpath=[os.path.join(fs.get_source_dir(), "builder", "tools")],
    variables=clivars,
    # Propagating External Environment
    ENV=os.environ,
    UNIX_TIME=int(time()),
    BUILD_DIR=os.path.join("$PROJECT_BUILD_DIR", "$ZXENV"),
    BUILD_SRC_DIR=os.path.join("$BUILD_DIR", "src"),
    BUILD_TEST_DIR=os.path.join("$BUILD_DIR", "test"),
    COMPILATIONDB_PATH=os.path.join("$PROJECT_DIR", "compile_commands.json"),
    LIBPATH=["$BUILD_DIR"],
    PROGNAME="program",
    PROGPATH=os.path.join("$BUILD_DIR", "$PROGNAME$PROGSUFFIX"),
    PROG_PATH="$PROGPATH",  # deprecated
    PYTHONEXE=get_pythonexe_path(),
)

# Declare command verbose messages
command_strings = dict(
    ARCOM="Archiving",
    LINKCOM="Linking",
    RANLIBCOM="Indexing",
    ASCOM="Compiling",
    ASPPCOM="Compiling",
    CCCOM="Compiling",
    CXXCOM="Compiling",
)
if not int(ARGUMENTS.get("ZXVERBOSE", 0)):
    for name, value in command_strings.items():
        DEFAULT_ENV_OPTIONS["%sSTR" % name] = "%s $TARGET" % (value)

env = DefaultEnvironment(**DEFAULT_ENV_OPTIONS)
env.SConscriptChdir(False)

# Load variables from CLI
env.Replace(
    **{
        key: PlatformBase.decode_scons_arg(env[key])
        for key in list(clivars.keys())
        if key in env
    }
)

# Setup project optional directories
config = env.GetProjectConfig()
app.set_session_var("custom_project_conf", config.path)

env.Replace(
    PROJECT_DIR=get_project_dir(),
    PROJECT_CORE_DIR=config.get("zhixin", "core_dir"),
    PROJECT_PACKAGES_DIR=config.get("zhixin", "packages_dir"),
    PROJECT_WORKSPACE_DIR=config.get("zhixin", "workspace_dir"),
    PROJECT_LIBDEPS_DIR=config.get("zhixin", "libdeps_dir"),
    PROJECT_INCLUDE_DIR=config.get("zhixin", "include_dir"),
    PROJECT_SRC_DIR=config.get("zhixin", "src_dir"),
    PROJECTSRC_DIR="$PROJECT_SRC_DIR",  # legacy for dev/platform
    PROJECT_TEST_DIR=config.get("zhixin", "test_dir"),
    PROJECT_DATA_DIR=config.get("zhixin", "data_dir"),
    PROJECTDATA_DIR="$PROJECT_DATA_DIR",  # legacy for dev/platform
    PROJECT_BUILD_DIR=config.get("zhixin", "build_dir"),
    BUILD_TYPE=env.GetBuildType(),
    BUILD_CACHE_DIR=config.get("zhixin", "build_cache_dir"),
    LIBSOURCE_DIRS=[
        config.get("zhixin", "lib_dir"),
        os.path.join("$PROJECT_LIBDEPS_DIR", "$ZXENV"),
        config.get("zhixin", "globallib_dir"),
    ],
)

if int(ARGUMENTS.get("ISATTY", 0)):
    # pylint: disable=protected-access
    click._compat.isatty = lambda stream: True

if env.subst("$BUILD_CACHE_DIR"):
    if not os.path.isdir(env.subst("$BUILD_CACHE_DIR")):
        os.makedirs(env.subst("$BUILD_CACHE_DIR"))
    env.CacheDir("$BUILD_CACHE_DIR")

if not int(ARGUMENTS.get("ZXVERBOSE", 0)):
    click.echo("Verbose mode can be enabled via `-v, --verbose` option")

# Dynamically load dependent tools
if "compiledb" in COMMAND_LINE_TARGETS:
    env.Tool("compilation_db")

if not os.path.isdir(env.subst("$BUILD_DIR")):
    os.makedirs(env.subst("$BUILD_DIR"))

env.LoadProjectOptions()
env.LoadZxPlatform()

env.SConsignFile(
    os.path.join(
        "$BUILD_CACHE_DIR" if env.subst("$BUILD_CACHE_DIR") else "$BUILD_DIR",
        ".sconsign%d%d" % (sys.version_info[0], sys.version_info[1]),
    )
)

env.SConscript(env.GetExtraScripts("pre"), exports="env")

if env.IsCleanTarget():
    env.CleanProject(fullclean=int(ARGUMENTS.get("FULLCLEAN", 0)))
    env.Exit(0)

env.SConscript("$BUILD_SCRIPT")

if "UPLOAD_FLAGS" in env:
    env.Prepend(UPLOADERFLAGS=["$UPLOAD_FLAGS"])
if env.GetProjectOption("upload_command"):
    env.Replace(UPLOADCMD=env.GetProjectOption("upload_command"))

env.SConscript(env.GetExtraScripts("post"), exports="env")

##############################################################################

# Checking program size
if env.get("SIZETOOL") and not (
    set(["nobuild", "sizedata"]) & set(COMMAND_LINE_TARGETS)
):
    env.Depends("upload", "checkprogsize")
    # Replace platform's "size" target with our
    _new_targets = [t for t in DEFAULT_TARGETS if str(t) != "size"]
    Default(None)
    Default(_new_targets)
    Default("checkprogsize")

if "compiledb" in COMMAND_LINE_TARGETS:
    env.Alias("compiledb", env.CompilationDatabase("$COMPILATIONDB_PATH"))

# Print configured protocols
env.AddPreAction(
    "upload",
    env.VerboseAction(
        lambda source, target, env: env.PrintUploadInfo(),
        "Configuring upload protocol...",
    ),
)

AlwaysBuild(env.Alias("__debug", DEFAULT_TARGETS))
AlwaysBuild(env.Alias("__test", DEFAULT_TARGETS))

env.ProcessDelayedActions()

##############################################################################

if "envdump" in COMMAND_LINE_TARGETS:
    click.echo(env.Dump())
    env.Exit(0)

if env.IsIntegrationDump():
    projenv = None
    try:
        Import("projenv")
    except:  # pylint: disable=bare-except
        projenv = env
    data = projenv.DumpIntegrationData(env)
    # dump to file for the further reading by project.helpers.load_build_metadata
    with open(
        projenv.subst(os.path.join("$BUILD_DIR", "idedata.json")),
        mode="w",
        encoding="utf8",
    ) as fp:
        json.dump(data, fp)
    click.echo("\n%s\n" % json.dumps(data))  # pylint: disable=undefined-variable
    env.Exit(0)

if "sizedata" in COMMAND_LINE_TARGETS:
    AlwaysBuild(
        env.Alias(
            "sizedata",
            DEFAULT_TARGETS,
            env.VerboseAction(env.DumpSizeData, "Generating memory usage report..."),
        )
    )

    Default("sizedata")

# issue #4604: process targets sequentially
for index, target in enumerate(
    [t for t in COMMAND_LINE_TARGETS if not t.startswith("__")][1:]
):
    env.Depends(target, COMMAND_LINE_TARGETS[index])
