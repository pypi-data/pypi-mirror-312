import os

import semantic_version

from zhixin import __version__, fs
from zhixin.package.manager.tool import ToolPackageManager
from zhixin.package.version import pepver_to_semver
from zhixin.platform._packages import PlatformPackagesMixin
from zhixin.platform._run import PlatformRunMixin
from zhixin.platform.board import PlatformBoardConfig
from zhixin.platform.exception import IncompatiblePlatform, UnknownBoard
from zhixin.project.config import ProjectConfig


class PlatformBase(  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    PlatformPackagesMixin, PlatformRunMixin
):
    CORE_SEMVER = pepver_to_semver(__version__)
    _BOARDS_CACHE = {}

    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.project_env = None  # set by factory.from_env(env)
        self.silent = False
        self.verbose = False

        self._manifest = fs.load_json(manifest_path)
        self._BOARDS_CACHE = {}
        self._custom_packages = None

        self.config = ProjectConfig.get_instance()
        self.pm = ToolPackageManager(self.config.get("zhixin", "packages_dir"))

    @property
    def name(self):
        return self._manifest["name"]

    @property
    def title(self):
        return self._manifest["title"]

    @property
    def description(self):
        return self._manifest["description"]

    @property
    def version(self):
        return self._manifest["version"]

    @property
    def homepage(self):
        return self._manifest.get("homepage")

    @property
    def repository_url(self):
        return self._manifest.get("repository", {}).get("url")

    @property
    def license(self):
        return self._manifest.get("license")

    @property
    def frameworks(self):
        return self._manifest.get("frameworks")

    @property
    def engines(self):
        return self._manifest.get("engines")

    @property
    def manifest(self):
        return self._manifest

    @property
    def packages(self):
        packages = self._manifest.get("packages", {})
        for item in self._custom_packages or []:
            name = item
            version = "*"
            if "@" in item:
                name, version = item.split("@", 1)
            spec = self.pm.ensure_spec(name)
            options = {"version": version.strip(), "optional": False}
            if spec.owner:
                options["owner"] = spec.owner
            if spec.name not in packages:
                packages[spec.name] = {}
            packages[spec.name].update(**options)
        return packages

    def ensure_engine_compatible(self):
        if not self.engines or "zhixin" not in self.engines:
            return True
        core_spec = semantic_version.SimpleSpec(self.engines["zhixin"])
        if self.CORE_SEMVER in core_spec:
            return True
        # ZX Core 6 is compatible with dev-platforms for ZX Core 2.0, 3.0, 4.0
        if any(
            semantic_version.Version.coerce(str(v)) in core_spec for v in (2, 3, 4, 5)
        ):
            return True
        raise IncompatiblePlatform(self.name, str(self.CORE_SEMVER), str(core_spec))

    def get_dir(self):
        return os.path.dirname(self.manifest_path)

    def get_build_script(self):
        main_script = os.path.join(self.get_dir(), "builder", "main.py")
        if os.path.isfile(main_script):
            return main_script
        raise NotImplementedError()

    def is_embedded(self):
        for opts in self.packages.values():
            if opts.get("type") == "uploader":
                return True
        return False

    def get_boards(self, id_=None):
        def _append_board(board_id, manifest_path):
            config = PlatformBoardConfig(manifest_path)
            if "platform" in config and config.get("platform") != self.name:
                return
            if "platforms" in config and self.name not in config.get("platforms"):
                return
            config.manifest["platform"] = self.name
            self._BOARDS_CACHE[board_id] = config

        bdirs = [
            self.config.get("zhixin", "boards_dir"),
            os.path.join(self.config.get("zhixin", "core_dir"), "boards"),
            os.path.join(self.get_dir(), "boards"),
        ]

        if id_ is None:
            for boards_dir in bdirs:
                if not os.path.isdir(boards_dir):
                    continue
                for item in sorted(os.listdir(boards_dir)):
                    _id = item[:-5]
                    if not item.endswith(".json") or _id in self._BOARDS_CACHE:
                        continue
                    _append_board(_id, os.path.join(boards_dir, item))
        else:
            if id_ not in self._BOARDS_CACHE:
                for boards_dir in bdirs:
                    if not os.path.isdir(boards_dir):
                        continue
                    manifest_path = os.path.join(boards_dir, "%s.json" % id_)
                    if os.path.isfile(manifest_path):
                        _append_board(id_, manifest_path)
                        break
            if id_ not in self._BOARDS_CACHE:
                raise UnknownBoard(id_)
        return self._BOARDS_CACHE[id_] if id_ else self._BOARDS_CACHE

    def board_config(self, id_):
        assert id_
        return self.get_boards(id_)

    def get_package_type(self, name):
        return self.packages[name].get("type")

    def configure_project_packages(self, env, targets=None):
        options = self.config.items(env=env, as_dict=True)
        if "framework" in options:
            # support ZX Core 3.0 dev/platforms
            options["zxframework"] = options["framework"]
        # override user custom packages
        self._custom_packages = options.get("platform_packages")
        self.configure_default_packages(options, targets or [])

    def configure_default_packages(self, options, targets):
        # enable used frameworks
        for framework in options.get("framework", []):
            if not self.frameworks:
                continue
            framework = framework.lower().strip()
            if not framework or framework not in self.frameworks:
                continue
            _pkg_name = self.frameworks[framework].get("package")
            if _pkg_name:
                self.packages[_pkg_name]["optional"] = False

        # enable upload tools for upload targets
        if any(["upload" in t for t in targets] + ["program" in targets]):
            for name, opts in self.packages.items():
                if opts.get("type") == "uploader":
                    self.packages[name]["optional"] = False
                # skip all packages in "nobuild" mode
                # allow only upload tools and frameworks
                elif "nobuild" in targets and opts.get("type") != "framework":
                    self.packages[name]["optional"] = True

    def configure_debug_session(self, debug_config):
        raise NotImplementedError

    def generate_sample_code(self, project_config, environment):
        raise NotImplementedError

    def on_installed(self):
        pass

    def on_uninstalled(self):
        pass

    def get_lib_storages(self):
        storages = {}
        for opts in (self.frameworks or {}).values():
            if "package" not in opts:
                continue
            pkg = self.get_package(opts["package"])
            if not pkg or not os.path.isdir(os.path.join(pkg.path, "libraries")):
                continue
            libs_dir = os.path.join(pkg.path, "libraries")
            storages[libs_dir] = opts["package"]
            libcores_dir = os.path.join(libs_dir, "__cores__")
            if not os.path.isdir(libcores_dir):
                continue
            for item in os.listdir(libcores_dir):
                libcore_dir = os.path.join(libcores_dir, item)
                if not os.path.isdir(libcore_dir):
                    continue
                storages[libcore_dir] = "%s-core-%s" % (opts["package"], item)

        return [dict(name=name, path=path) for path, name in storages.items()]
