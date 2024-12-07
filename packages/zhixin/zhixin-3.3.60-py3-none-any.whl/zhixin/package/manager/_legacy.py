import os

from zhixin import fs
from zhixin.package.meta import PackageItem, PackageSpec


class PackageManagerLegacyMixin:
    def build_legacy_spec(self, pkg_dir):
        # find src manifest
        src_manifest_name = ".zxpkgmanager.json"
        src_manifest_path = None
        for name in os.listdir(pkg_dir):
            if not os.path.isfile(os.path.join(pkg_dir, name, src_manifest_name)):
                continue
            src_manifest_path = os.path.join(pkg_dir, name, src_manifest_name)
            break

        if src_manifest_path:
            src_manifest = fs.load_json(src_manifest_path)
            return PackageSpec(
                name=src_manifest.get("name"),
                uri=src_manifest.get("url"),
                requirements=src_manifest.get("requirements"),
            )

        # fall back to a package manifest
        manifest = self.load_manifest(pkg_dir)
        return PackageSpec(name=manifest.get("name"))

    def legacy_load_manifest(self, pkg):
        if not isinstance(pkg, PackageItem):
            assert os.path.isdir(pkg)
            pkg = PackageItem(pkg)
        manifest = self.load_manifest(pkg)
        manifest["__pkg_dir"] = pkg.path
        for key in ("name", "version"):
            if not manifest.get(key):
                manifest[key] = str(getattr(pkg.metadata, key))
        if pkg.metadata and pkg.metadata.spec and pkg.metadata.spec.external:
            manifest["__src_url"] = pkg.metadata.spec.uri
            manifest["version"] = str(pkg.metadata.version)
        if pkg.metadata and pkg.metadata.spec.owner:
            manifest["ownername"] = pkg.metadata.spec.owner
        return manifest

    def legacy_get_installed(self):
        return [self.legacy_load_manifest(pkg) for pkg in self.get_installed()]
