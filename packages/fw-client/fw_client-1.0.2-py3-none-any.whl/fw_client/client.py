"""Flywheel HTTP API sync client."""

import asyncio
import os
import random
import re
import time
import typing as t
from functools import cached_property

import backoff
import httpx
from fw_utils import AttrDict
from packaging import version

from . import common
from .errors import ValidationError


class FWClientMetaClass(type):
    """Change class inheritance to help defining base class for sync/async client."""

    def __new__(cls, name, bases, class_dict):
        """Inject extra base class when creating client instance."""
        if "base_class" in class_dict:
            base_class = class_dict["base_class"]
            bases = (bases[0], base_class) if bases else (base_class,)
        return super().__new__(cls, name, bases, class_dict)


class FWClientBase(metaclass=FWClientMetaClass):
    """Flywheel HTTP API base client."""

    def __init__(  # noqa: PLR0912, PLR0913, PLR0915
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        client_name: str | None = None,
        client_version: str | None = None,
        client_info: dict[str, str] | None = None,
        io_proxy_url: str | None = None,
        snapshot_url: str | None = None,
        xfer_url: str | None = None,
        drone_secret: str | None = None,
        device_type: str | None = None,
        device_label: str | None = None,
        defer_auth: bool = False,
        core_features: t.Sequence[str] = common.CORE_FEATURES,
        retry_allowed_methods: t.Sequence[str] = common.RETRY_METHODS,
        retry_status_forcelist: t.Sequence[int] = common.RETRY_STATUSES,
        retry_backoff_factor: float = 0.5,
        retry_total: int = 5,
        **kwargs,
    ):
        """Initialize FW client."""
        self._cache: dict[str, tuple[t.Any, float]] = {}
        self.core_features = core_features
        self.defer_auth = defer_auth
        self.drone_secret = drone_secret
        self.device_type = device_type or client_name
        self.device_label = device_label
        self.retry_backoff_factor = retry_backoff_factor
        self.retry_allowed_methods = retry_allowed_methods
        self.retry_status_forcelist = retry_status_forcelist
        self.retry_total = retry_total
        if not (api_key or base_url):
            raise ValidationError("api_key or base_url required")
        # extract any additional key info "[type ][scheme://]host[:port]:key"
        if api_key:
            match = common.API_KEY_RE.match(t.cast(str, api_key))
            if not match:  # pragma: no cover
                raise ValidationError(f"invalid api_key: {api_key!r}")
            info = match.groupdict()
            # clean the key of extras (enhanced keys don't allow any)
            api_key = info["api_key"]
            # use site url prefixed on the key if otherwise not provided
            if not base_url:
                if not info["host"]:
                    raise ValidationError("api_key with host required")
                scheme = info["scheme"] or "https://"
                host = info["host"]
                port = info["port"] or ""
                base_url = f"{scheme}{host}{port}"
        if not base_url:  # pragma: no cover
            raise ValidationError("base_url required")
        if not base_url.startswith("http"):
            base_url = f"https://{base_url}"
        # strip url /api path suffix if present to accommodate other apis
        base_url = re.sub(r"(/api)?/?$", "", base_url)
        headers = kwargs.setdefault("headers", {})
        # require auth (unless it's deferred via defer_auth)
        creds = api_key or self.drone_secret
        if self.defer_auth and creds:
            msg = "api_key and drone_secret not allowed with defer_auth"
            raise ValidationError(msg)
        elif not self.defer_auth and not creds:
            raise ValidationError("api_key or drone_secret required")
        if api_key:
            # careful, core-api is case-sensitively testing for Bearer...
            key_type = "Bearer" if len(api_key) == 57 else "scitran-user"
            headers["Authorization"] = f"{key_type} {api_key}"
        # require device_type and device_label if drone
        elif not api_key and self.drone_secret:
            if not self.device_type:  # pragma: no cover
                raise ValidationError("device_type required")
            if not self.device_label:  # pragma: no cover
                raise ValidationError("device_label required")
        client_info = client_info or {}
        client_info |= {client_name: client_version} if client_name else {}
        headers["User-Agent"] = common.dump_useragent(**client_info)
        self.svc_urls = {
            "/api": base_url,
            "/io-proxy": io_proxy_url,
            "/snapshot": snapshot_url,
            "/xfer": xfer_url,
        }
        kwargs["base_url"] = base_url
        kwargs.setdefault("timeout", httpx.Timeout(10, read=30))
        kwargs.setdefault("transport", self.transport_class(http2=True, retries=3))
        kwargs.setdefault("follow_redirects", True)
        super().__init__(**kwargs)

    @cached_property
    def retry_decorators(self) -> tuple[t.Callable, t.Callable]:
        """Return configured http and transport error retry decorators."""

        def retry_when(response: httpx.Response):
            method = response.request.method in self.retry_allowed_methods
            status = response.status_code in self.retry_status_forcelist
            # only requests with byte stream can be safely retried
            byte_stream = isinstance(response.request.stream, httpx.ByteStream)
            return method and status and byte_stream

        # in backoff max tries includes the initial request, so add 1
        # because 0 means infinite tries
        retry_http_error = backoff.on_predicate(
            backoff.expo,
            retry_when,
            max_tries=self.retry_total + 1,
            factor=self.retry_backoff_factor,
        )
        retry_transport_error = backoff.on_exception(
            backoff.expo,
            httpx.TransportError,
            max_tries=self.retry_total + 1,
            factor=self.retry_backoff_factor,
        )
        return retry_http_error, retry_transport_error

    def prepare_request(self, url: str, kwargs: dict) -> tuple[str, dict]:
        """Prepare request url and headers."""
        # dispatch known service prefixes to cluster-internal urls
        if not url.startswith("http"):
            svc_prefix = re.sub(r"^(/[^/]+)?.*$", r"\1", url)
            # use service base url if defined
            if self.svc_urls.get(svc_prefix):
                url = f"{self.svc_urls[svc_prefix]}{url}"
            # otherwise default to self.base_url IFF looks like a domain
            elif re.match(r".*\.[a-z]{2,}", str(self.base_url)):
                url = f"{self.base_url}{url}"  # pragma: no cover
            # raise error about missing service url for known prefixes/APIs
            elif svc_prefix in self.svc_urls:
                svc_name = f"{svc_prefix[1:]}".replace("-", "_")
                msg = f"{svc_name}_url required for {svc_prefix} requests"
                raise ValueError(f"{self.__class__.__name__}: {msg}")
            # raise error about invalid path for unknown prefixes
            else:
                msg = f"invalid URL path prefix: {svc_prefix}"
                raise ValueError(f"{self.__class__.__name__}: {msg}")
        # send anonymous request when the auth header is explicitly set to None
        headers = kwargs["headers"] = kwargs.get("headers") or {}
        if kwargs.get("auth") is None and headers.get("Authorization", ...) is None:
            kwargs["auth"] = common.httpx_anon
            headers.pop("Authorization")  # httpx raises on None
        # set authorization header from simple str auth kwarg
        if isinstance(kwargs.get("auth"), str):
            headers["Authorization"] = kwargs.pop("auth")
        # set default feature headers for core-api
        if "/api/" in url:
            headers.setdefault("X-Accept-Feature", ", ".join(self.core_features))
        return url, kwargs


class FWClient(FWClientBase):
    """Flywheel sync HTTP API Client."""

    base_class = httpx.Client
    transport_class = httpx.HTTPTransport

    @cached_property
    def retry(self):
        """Return retry function."""
        retry_http_error, retry_transport_error = self.retry_decorators

        @retry_http_error
        @retry_transport_error
        def retry_errors(func, *args, **kwargs):
            return func(*args, **kwargs)

        return retry_errors

    def _get_device_key(self) -> str:
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
                time.sleep(random.random())  # pragma: no cover
            # furthermore, delete redundant device entries, leaving only the 1st
            # ie. try to enforce type/label uniqueness from the client side
            type_filter = f"type={self.device_type}"
            label_filter = f"label={self.device_label}"
            query = f"filter={type_filter}&filter={label_filter}"
            url = "/api/devices"
            devices = self.get(f"{url}?{query}", **kwargs)
            for device in devices[1:]:  # type: ignore
                self.delete(f"{url}/{device._id}", **kwargs)
            # legacy api keys are auto-generated and returned on the response
            # TODO generate key if not exposed after devices get enhanced keys
            # NOTE caching will need rework and move to self due to expiration
            device = self.get(f"{url}/self", **kwargs)
            common.DRONE_DEVICE_KEYS[drone] = device.key
        return common.DRONE_DEVICE_KEYS[drone]

    def _cached_get(self, path: str) -> AttrDict:
        """Return GET response cached with a one hour TTL."""
        now = time.time()
        val, exp = self._cache.get(path, (None, 0))
        if not val or now > exp:
            val = self.get(path)
            self._cache[path] = val, now + common.CACHE_TTL
        return val

    def get_core_config(self) -> AttrDict:
        """Return Core's configuration."""
        return self._cached_get("/api/config")

    def get_core_version(self) -> str | None:
        """Return Core's release version."""
        return self._cached_get("/api/version").get("release")

    def get_auth_status(self) -> AttrDict:
        """Return the client's auth status."""
        status = self._cached_get("/api/auth/status")
        resource = "devices" if status.is_device else "users"
        status["info"] = self._cached_get(f"/api/{resource}/self")
        return status

    def check_feature(self, feature: str) -> bool:
        """Return True if Core has the given feature and it's enabled."""
        features = self.get_core_config().features
        return bool(features.get(feature))  # type: ignore

    def check_version(self, min_ver: str) -> bool:
        """Return True if Core's version is greater or equal to 'min_ver'."""
        if not (core_version := self.get_core_version()):
            # assume latest on dev deployments without a version
            return True
        return version.parse(core_version) >= version.parse(min_ver)

    def request(self, method: str, url: str, raw: bool = False, **kwargs):  # type: ignore
        """Send request and return loaded JSON response."""
        need_auth = kwargs.get("auth", True) and "Authorization" not in self.headers
        if not self.defer_auth and need_auth:
            api_key = self._get_device_key()
            key_type = "Bearer" if len(api_key) == 57 else "scitran-user"
            self.headers["Authorization"] = f"{key_type} {api_key}"
        url, kwargs = self.prepare_request(url, kwargs)
        response = self.retry(super().request, method, url, **kwargs)
        response.__class__ = common.Response
        # return response when raw=True
        if raw:
            return response
        # raise if there was an http error (eg. 404)
        response.raise_for_status()
        # don't load empty response as json
        if not response.content:
            return None
        return response.json()

    def get(self, url: str, **kwargs):  # type: ignore
        """Send a `GET` request."""
        return self.request("GET", url, **kwargs)

    def options(self, url: str, **kwargs):  # type: ignore
        """Send a `OPTIONS` request."""
        return self.request("OPTIONS", url, **kwargs)  # pragma: no cover

    def head(self, url: str, **kwargs):  # type: ignore
        """Send a `HEAD` request."""
        return self.request("HEAD", url, **kwargs)  # pragma: no cover

    def post(self, url: str, **kwargs):  # type: ignore
        """Send a `POST` request."""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):  # type: ignore
        """Send a `PUT` request."""
        return self.request("PUT", url, **kwargs)  # pragma: no cover

    def patch(self, url: str, **kwargs):  # type: ignore
        """Send a `PATCH` request."""
        return self.request("PATCH", url, **kwargs)  # pragma: no cover

    def delete(self, url: str, **kwargs):  # type: ignore
        """Send a `DELETE` request."""
        return self.request("DELETE", url, **kwargs)

    def upload_device_file(
        self,
        project_id: str,
        file: t.BinaryIO,
        origin: dict | None = None,
        content_encoding: str | None = None,
    ) -> str:
        """Upload a single file using the /api/storage/files endpoint (device only)."""
        auth_status = self.get_auth_status()
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
        response = self.post(url, params=params, headers=headers, raw=True)
        if response.is_success:
            upload = response.json()
            headers = upload.get("upload_headers") or {}
            if hasattr(file, "getbuffer"):
                headers["Content-Length"] = str(file.getbuffer().nbytes)
            else:
                headers["Content-Length"] = str(os.fstat(file.fileno()).st_size)
            try:

                def stream():
                    while chunk := file.read(common.MEGABYTE):
                        yield chunk

                self.put(
                    url=upload["upload_url"],
                    auth=common.httpx_anon,
                    headers=headers,
                    content=stream(),
                )
            # make sure we clean up any residue on failure
            except httpx.HTTPError:
                del_url = f"{url}/{upload['storage_file_id']}"
                self.delete(del_url, params={"ignore_storage_errors": True})
                raise
        # core's 409 means no signed url support - upload directly instead
        elif response.status_code == 409:
            del params["signed_url"]
            files = {"file": file}
            upload = self.post(url, params=params, headers=headers, files=files)
        else:
            response.raise_for_status()
        return upload["storage_file_id"]


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
                await asyncio.sleep(random.random())  # pragma: no cover
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

    async def get_core_version(self) -> str | None:
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
        response.__class__ = common.Response
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
        origin: dict | None = None,
        content_encoding: str | None = None,
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
                    auth=common.httpx_anon,
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
