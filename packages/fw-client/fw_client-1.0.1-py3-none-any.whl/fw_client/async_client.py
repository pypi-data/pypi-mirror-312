"""Flywheel HTTP API async client."""

import asyncio
import os
import time
import typing as t
from functools import cached_property
from random import random

import httpx
from fw_utils import AttrDict
from packaging import version

from . import common
from .base import FWClientBase
from .common import Response, httpx_anon


class FWClientAsync(FWClientBase):
    """Flywheel async HTTP API Client."""

    base_class = httpx.AsyncClient
    transport_class = httpx.AsyncHTTPTransport

    @cached_property
    def retry(self):
        """Return retry function."""
        retry_http_error, retry_transport_error = self.retry_decorators

        @retry_http_error
        @retry_transport_error
        async def retry_errors(func, *args, **kwargs):
            return await func(*args, **kwargs)

        return retry_errors

    async def _get_device_key(self) -> str:
        """Return device API key for the given drone_secret (cached)."""
        drone = (self.base_url, self.device_type, self.device_label)
        if drone not in common.DRONE_DEVICE_KEYS:
            # limit the use of the secret only for acquiring a device api key
            assert self.drone_secret and self.device_type and self.device_label
            headers = {
                "X-Scitran-Auth": self.drone_secret,
                "X-Scitran-Method": self.device_type,
                "X-Scitran-Name": self.device_label,
            }
            kwargs: t.Any = {"headers": headers, "auth": None}
            # core-api auto-creates new device entries based on type and label
            # however, it may create conflicting ones for parallel requests...
            # FLYW-17258 intended to fix and guard against that, to no avail
            # to mitigate, add some(0-1) jitter before the 1st connection
            if "PYTEST_CURRENT_TEST" not in os.environ:
                await asyncio.sleep(random())  # pragma: no cover
            # furthermore, delete redundant device entries, leaving only the 1st
            # ie. try to enforce type/label uniqueness from the client side
            type_filter = f"type={self.device_type}"
            label_filter = f"label={self.device_label}"
            query = f"filter={type_filter}&filter={label_filter}"
            url = "/api/devices"
            devices = await self.get(f"{url}?{query}", **kwargs)
            for device in devices[1:]:  # type: ignore
                await self.delete(f"{url}/{device._id}", **kwargs)
            # legacy api keys are auto-generated and returned on the response
            # TODO generate key if not exposed after devices get enhanced keys
            # NOTE caching will need rework and move to self due to expiration
            device = await self.get(f"{url}/self", **kwargs)
            common.DRONE_DEVICE_KEYS[drone] = device.key
        return common.DRONE_DEVICE_KEYS[drone]

    async def _cached_get(self, path: str) -> AttrDict:
        """Return GET response cached with a one hour TTL."""
        now = time.time()
        val, exp = self._cache.get(path, (None, 0))
        if not val or now > exp:
            val = await self.get(path)
            self._cache[path] = val, now + common.CACHE_TTL
        return val

    async def get_core_config(self) -> AttrDict:
        """Return Core's configuration."""
        return await self._cached_get("/api/config")

    async def get_core_version(self) -> t.Optional[str]:
        """Return Core's release version."""
        return (await self._cached_get("/api/version")).get("release")

    async def get_auth_status(self) -> AttrDict:
        """Return the client's auth status."""
        status = await self._cached_get("/api/auth/status")
        resource = "devices" if status.is_device else "users"
        status["info"] = await self._cached_get(f"/api/{resource}/self")
        return status

    async def check_feature(self, feature: str) -> bool:
        """Return True if Core has the given feature and it's enabled."""
        features = (await self.get_core_config()).features
        return bool(features.get(feature))  # type: ignore

    async def check_version(self, min_ver: str) -> bool:
        """Return True if Core's version is greater or equal to 'min_ver'."""
        if not (core_version := await self.get_core_version()):
            # assume latest on dev deployments without a version
            return True
        return version.parse(core_version) >= version.parse(min_ver)

    async def request(self, method: str, url: str, raw: bool = False, **kwargs):  # type: ignore
        """Send request and return loaded JSON response."""
        need_auth = kwargs.get("auth", True) and "Authorization" not in self.headers
        if not self.defer_auth and need_auth:
            api_key = await self._get_device_key()
            key_type = "Bearer" if len(api_key) == 57 else "scitran-user"
            self.headers["Authorization"] = f"{key_type} {api_key}"
        url, kwargs = self.prepare_request(url, kwargs)
        response = await self.retry(super().request, method, url, **kwargs)
        response.__class__ = Response
        # return response when raw=True
        if raw:
            return response
        # raise if there was an http error (eg. 404)
        response.raise_for_status()
        # don't load empty response as json
        if not response.content:
            return None
        return response.json()

    async def get(self, url: str, **kwargs):  # type: ignore
        """Send a `GET` request."""
        return await self.request("GET", url, **kwargs)

    async def options(self, url: str, **kwargs):  # type: ignore
        """Send a `OPTIONS` request."""
        return await self.request("OPTIONS", url, **kwargs)  # pragma: no cover

    async def head(self, url: str, **kwargs):  # type: ignore
        """Send a `HEAD` request."""
        return await self.request("HEAD", url, **kwargs)  # pragma: no cover

    async def post(self, url: str, **kwargs):  # type: ignore
        """Send a `POST` request."""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs):  # type: ignore
        """Send a `PUT` request."""
        return await self.request("PUT", url, **kwargs)  # pragma: no cover

    async def patch(self, url: str, **kwargs):  # type: ignore
        """Send a `PATCH` request."""
        return await self.request("PATCH", url, **kwargs)  # pragma: no cover

    async def delete(self, url: str, **kwargs):  # type: ignore
        """Send a `DELETE` request."""
        return await self.request("DELETE", url, **kwargs)

    async def upload_device_file(
        self,
        project_id: str,
        file: t.BinaryIO,
        origin: t.Optional[dict] = None,
        content_encoding: t.Optional[str] = None,
    ) -> str:
        """Upload a single file using the /api/storage/files endpoint (device only)."""
        auth_status = await self.get_auth_status()
        assert auth_status.is_device, "Device authentication required"
        url = "/api/storage/files"
        origin = origin or auth_status.origin
        params = {
            "project_id": project_id,
            "origin_type": origin["type"],
            "origin_id": origin["id"],
            "signed_url": True,
        }
        headers = {"Content-Encoding": content_encoding} if content_encoding else {}
        response = await self.post(url, params=params, headers=headers, raw=True)
        if response.is_success:
            upload = response.json()
            headers = upload.get("upload_headers") or {}
            if hasattr(file, "getbuffer"):
                headers["Content-Length"] = str(file.getbuffer().nbytes)
            else:
                headers["Content-Length"] = str(os.fstat(file.fileno()).st_size)
            try:

                async def stream():
                    while chunk := file.read(common.MEGABYTE):
                        yield chunk

                await self.put(
                    url=upload["upload_url"],
                    auth=httpx_anon,
                    headers=headers,
                    content=stream(),
                )
            # make sure we clean up any residue on failure
            except httpx.HTTPError:
                del_url = f"{url}/{upload['storage_file_id']}"
                await self.delete(del_url, params={"ignore_storage_errors": True})
                raise
        # core's 409 means no signed url support - upload directly instead
        elif response.status_code == 409:
            del params["signed_url"]
            files = {"file": file}
            upload = await self.post(url, params=params, headers=headers, files=files)
        else:
            response.raise_for_status()
        return upload["storage_file_id"]
