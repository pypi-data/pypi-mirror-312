import json
import os

from zhixin import fs
from zhixin.package.exception import PackageException
from zhixin.package.meta import PackageItem, PackageSpec


class PackageManagerSymlinkMixin:
    @staticmethod
    def is_symlink(path):
        return path and path.endswith(".zx-link") and os.path.isfile(path)

    @classmethod
    def resolve_symlink(cls, path):
        assert cls.is_symlink(path)
        data = fs.load_json(path)
        spec = PackageSpec(**data["spec"])
        assert spec.symlink
        pkg_dir = spec.uri[10:]
        if not os.path.isabs(pkg_dir):
            pkg_dir = os.path.normpath(os.path.join(data["cwd"], pkg_dir))
        return (pkg_dir if os.path.isdir(pkg_dir) else None, spec)

    def get_symlinked_package(self, path):
        pkg_dir, spec = self.resolve_symlink(path)
        if not pkg_dir:
            return None
        pkg = PackageItem(os.path.realpath(pkg_dir))
        if not pkg.metadata:
            pkg.metadata = self.build_metadata(pkg.path, spec)
        return pkg

    def install_symlink(self, spec):
        assert spec.symlink
        pkg_dir = spec.uri[10:]
        if not os.path.isdir(pkg_dir):
            raise PackageException(
                f"Can not create a symbolic link for `{pkg_dir}`, not a directory"
            )
        link_path = os.path.join(
            self.package_dir,
            "%s.zx-link" % (spec.name or os.path.basename(os.path.abspath(pkg_dir))),
        )
        with open(link_path, mode="w", encoding="utf-8") as fp:
            json.dump(dict(cwd=os.getcwd(), spec=spec.as_dict()), fp)
        return self.get_symlinked_package(link_path)

    def uninstall_symlink(self, spec):
        assert spec.symlink
        for name in os.listdir(self.package_dir):
            path = os.path.join(self.package_dir, name)
            if not self.is_symlink(path):
                continue
            pkg = self.get_symlinked_package(path)
            if pkg.metadata.spec.uri == spec.uri:
                os.remove(path)
