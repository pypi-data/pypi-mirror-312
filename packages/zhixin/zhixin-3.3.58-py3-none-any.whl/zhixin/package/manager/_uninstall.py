import os
import shutil

import click

from zhixin import fs
from zhixin.package.exception import UnknownPackageError
from zhixin.package.meta import PackageItem, PackageSpec


class PackageManagerUninstallMixin:
    def uninstall(self, spec, skip_dependencies=False):
        try:
            self.lock()
            return self._uninstall(spec, skip_dependencies)
        finally:
            self.unlock()

    def _uninstall(self, spec, skip_dependencies=False):
        pkg = self.get_package(spec)
        if not pkg or not pkg.metadata:
            raise UnknownPackageError(spec)

        uninstalled_pkgs = self.memcache_get("__uninstalled_pkgs", [])
        if uninstalled_pkgs and pkg.path in uninstalled_pkgs:
            return pkg
        uninstalled_pkgs.append(pkg.path)
        self.memcache_set("__uninstalled_pkgs", uninstalled_pkgs)

        self.log.info(
            "Removing %s @ %s"
            % (click.style(pkg.metadata.name, fg="cyan"), pkg.metadata.version)
        )

        self.call_pkg_script(pkg, "preuninstall")

        # firstly, remove dependencies
        if not skip_dependencies:
            self.uninstall_dependencies(pkg)

        if pkg.metadata.spec.symlink:
            self.uninstall_symlink(pkg.metadata.spec)
        elif os.path.islink(pkg.path):
            os.unlink(pkg.path)
        else:
            fs.rmtree(pkg.path)
        self.memcache_reset()

        # unfix detached-package with the same name
        detached_pkg = self.get_package(PackageSpec(name=pkg.metadata.name))
        if (
            detached_pkg
            and "@" in detached_pkg.path
            and not os.path.isdir(
                os.path.join(self.package_dir, detached_pkg.get_safe_dirname())
            )
        ):
            shutil.move(
                detached_pkg.path,
                os.path.join(self.package_dir, detached_pkg.get_safe_dirname()),
            )
            self.memcache_reset()

        self.log.info(
            click.style(
                "{name}@{version} has been removed!".format(**pkg.metadata.as_dict()),
                fg="green",
            )
        )

        return pkg

    def uninstall_dependencies(self, pkg):
        assert isinstance(pkg, PackageItem)
        dependencies = self.get_pkg_dependencies(pkg)
        if not dependencies:
            return
        self.log.info("Removing dependencies...")
        for dependency in dependencies:
            pkg = self.get_package(self.dependency_to_spec(dependency))
            if not pkg:
                continue
            self._uninstall(pkg)
