import json
import os

from zhixin import util
from zhixin.package.exception import MissingPackageManifestError
from zhixin.package.manager.base import BasePackageManager
from zhixin.package.meta import PackageSpec, PackageType
from zhixin.platform.factory import PlatformFactory
from zhixin.project.config import ProjectConfig


class LibraryPackageManager(BasePackageManager):  # pylint: disable=too-many-ancestors
    def __init__(self, package_dir=None, **kwargs):
        super().__init__(
            PackageType.LIBRARY,
            package_dir
            or ProjectConfig.get_instance().get("zhixin", "globallib_dir"),
            **kwargs
        )

    @property
    def manifest_names(self):
        return PackageType.get_manifest_map()[PackageType.LIBRARY]

    def find_pkg_root(self, path, spec):
        try:
            return super().find_pkg_root(path, spec)
        except MissingPackageManifestError:
            pass
        assert isinstance(spec, PackageSpec)

        root_dir = self.find_library_root(path)

        # automatically generate library manifest
        with open(
            os.path.join(root_dir, "library.json"), mode="w", encoding="utf8"
        ) as fp:
            json.dump(
                dict(
                    name=spec.name,
                    version=self.generate_rand_version(),
                ),
                fp,
                indent=2,
            )

        return root_dir

    @staticmethod
    def find_library_root(path):
        root_dir_signs = set(["include", "Include", "inc", "Inc", "src", "Src"])
        root_file_signs = set(
            [
                "conanfile.py",  # Conan-based library
                "CMakeLists.txt",  # CMake-based library
            ]
        )
        for root, dirs, files in os.walk(path):
            if not files and len(dirs) == 1:
                continue
            if set(root_dir_signs) & set(dirs):
                return root
            if set(root_file_signs) & set(files):
                return root
            for fname in files:
                if fname.endswith((".c", ".cpp", ".h", ".hpp", ".S")):
                    return root
        return path

    def install_dependency(self, dependency):
        spec = self.dependency_to_spec(dependency)
        # skip built-in dependencies
        not_builtin_conds = [spec.external, spec.owner]
        if not any(not_builtin_conds):
            not_builtin_conds.append(not self.is_builtin_lib(spec.name))
        if any(not_builtin_conds):
            return super().install_dependency(dependency)
        return None

    @staticmethod
    @util.memoized(expire="60s")
    def get_builtin_libs(storage_names=None):
        # pylint: disable=import-outside-toplevel
        from zhixin.package.manager.platform import PlatformPackageManager

        items = []
        storage_names = storage_names or []
        pm = PlatformPackageManager()
        for pkg in pm.get_installed():
            p = PlatformFactory.new(pkg)
            for storage in p.get_lib_storages():
                if storage_names and storage["name"] not in storage_names:
                    continue
                lm = LibraryPackageManager(storage["path"])
                items.append(
                    {
                        "name": storage["name"],
                        "path": storage["path"],
                        "items": lm.legacy_get_installed(),
                    }
                )
        return items

    @classmethod
    def is_builtin_lib(cls, name):
        for storage in cls.get_builtin_libs():
            for lib in storage["items"]:
                if lib.get("name") == name:
                    return True
        return False
