import hashlib
import logging
import os
import tempfile
import time

import click

from zhixin import app, compat, util
from zhixin.package.download import FileDownloader
from zhixin.package.lockfile import LockFile


class PackageManagerDownloadMixin:
    DOWNLOAD_CACHE_EXPIRE = 86400 * 30  # keep package in a local cache for 1 month

    def compute_download_path(self, *args):
        request_hash = hashlib.new("sha1")
        for arg in args:
            request_hash.update(compat.hashlib_encode_data(arg))
        dl_path = os.path.join(self.get_download_dir(), request_hash.hexdigest())
        return dl_path

    def get_download_usagedb_path(self):
        return os.path.join(self.get_download_dir(), "usage.db")

    def set_download_utime(self, path, utime=None):
        with app.State(self.get_download_usagedb_path(), lock=True) as state:
            state[os.path.basename(path)] = int(time.time() if not utime else utime)

    @util.memoized(DOWNLOAD_CACHE_EXPIRE)
    def cleanup_expired_downloads(self, _=None):
        with app.State(self.get_download_usagedb_path(), lock=True) as state:
            # remove outdated
            for fname in list(state.keys()):
                if state[fname] > (time.time() - self.DOWNLOAD_CACHE_EXPIRE):
                    continue
                del state[fname]
                dl_path = os.path.join(self.get_download_dir(), fname)
                if os.path.isfile(dl_path):
                    os.remove(dl_path)

    def download(self, url, checksum=None):
        silent = not self.log.isEnabledFor(logging.INFO)
        dl_path = self.compute_download_path(url, checksum or "")
        if os.path.isfile(dl_path):
            self.set_download_utime(dl_path)
            return dl_path

        with_progress = not app.is_disabled_progressbar()
        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.get_download_dir())
        try:
            with LockFile(dl_path):
                try:
                    fd = FileDownloader(url)
                    fd.set_destination(tmp_path)
                    fd.start(with_progress=with_progress, silent=silent)
                except IOError as exc:
                    raise_error = not silent
                    if with_progress:
                        try:
                            fd = FileDownloader(url)
                            fd.set_destination(tmp_path)
                            fd.start(with_progress=False, silent=silent)
                        except IOError:
                            raise_error = True
                    if raise_error:
                        self.log.error(
                            click.style(
                                "Error: Please read https://bit.ly/package-manager-ioerror",
                                fg="red",
                            )
                        )
                        raise exc
            if checksum:
                fd.verify(checksum)
            os.close(tmp_fd)
            os.rename(tmp_path, dl_path)
        finally:
            if os.path.isfile(tmp_path):
                os.close(tmp_fd)
                os.remove(tmp_path)

        assert os.path.isfile(dl_path)
        self.set_download_utime(dl_path)
        return dl_path
