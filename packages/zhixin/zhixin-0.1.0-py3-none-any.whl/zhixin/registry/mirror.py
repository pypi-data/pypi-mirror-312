import json
from urllib.parse import urlparse

from zhixin import __registry_mirror_hosts__
from zhixin.cache import ContentCache
from zhixin.http import HTTPClient
from zhixin.registry.client import RegistryClient


class RegistryFileMirrorIterator:
    HTTP_CLIENT_INSTANCES = {}

    def __init__(self, download_url):
        self.download_url = download_url
        self._url_parts = urlparse(download_url)
        self._mirror = "%s://%s" % (self._url_parts.scheme, self._url_parts.netloc)
        self._visited_mirrors = []

    def __iter__(self):  # pylint: disable=non-iterator-returned
        return self

    def __next__(self):
        cache_key = ContentCache.key_from_args(
            "head", self.download_url, self._visited_mirrors
        )
        with ContentCache("http") as cc:
            result = cc.get(cache_key)
            if result is not None:
                try:
                    headers = json.loads(result)
                    return (
                        headers["Location"],
                        headers["X-ZX-Content-SHA256"],
                    )
                except (ValueError, KeyError):
                    pass

            http = self.get_http_client()
            response = http.send_request(
                "head",
                self._url_parts.path,
                allow_redirects=False,
                params=(
                    dict(bypass=",".join(self._visited_mirrors))
                    if self._visited_mirrors
                    else None
                ),
                x_with_authorization=RegistryClient.allowed_private_packages(),
            )
            stop_conditions = [
                response.status_code not in (302, 307),
                not response.headers.get("Location"),
                not response.headers.get("X-ZX-Mirror"),
                response.headers.get("X-ZX-Mirror") in self._visited_mirrors,
            ]
            if any(stop_conditions):
                raise StopIteration
            self._visited_mirrors.append(response.headers.get("X-ZX-Mirror"))
            cc.set(
                cache_key,
                json.dumps(
                    {
                        "Location": response.headers.get("Location"),
                        "X-ZX-Content-SHA256": response.headers.get(
                            "X-ZX-Content-SHA256"
                        ),
                    }
                ),
                "1h",
            )
            return (
                response.headers.get("Location"),
                response.headers.get("X-ZX-Content-SHA256"),
            )

    def get_http_client(self):
        if self._mirror not in RegistryFileMirrorIterator.HTTP_CLIENT_INSTANCES:
            endpoints = [self._mirror]
            for host in __registry_mirror_hosts__:
                endpoint = f"https://dl.{host}"
                if endpoint not in endpoints:
                    endpoints.append(endpoint)
            RegistryFileMirrorIterator.HTTP_CLIENT_INSTANCES[self._mirror] = HTTPClient(
                endpoints
            )
        return RegistryFileMirrorIterator.HTTP_CLIENT_INSTANCES[self._mirror]
