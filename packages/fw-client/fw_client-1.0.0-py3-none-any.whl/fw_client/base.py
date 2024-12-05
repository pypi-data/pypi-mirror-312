"""Flywheel HTTP API base module defining common interfaces."""

import re
import typing as t
from functools import cached_property
from importlib.metadata import version as pkg_version

import backoff
import httpx

from . import common
from .common import dump_useragent
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
        api_key: t.Optional[str] = None,
        base_url: t.Optional[str] = None,
        client_name: str = "fw-client",
        client_version: str = pkg_version("fw_client"),
        client_info: t.Dict[str, str] = {},
        io_proxy_url: t.Optional[str] = None,
        snapshot_url: t.Optional[str] = None,
        xfer_url: t.Optional[str] = None,
        drone_secret: t.Optional[str] = None,
        device_type: t.Optional[str] = None,
        device_label: t.Optional[str] = None,
        defer_auth: bool = False,
        retry_backoff_factor: float = 0.5,
        retry_allowed_methods: t.Sequence[str] = common.RETRY_METHODS,
        retry_status_forcelist: t.Sequence[int] = common.RETRY_STATUSES,
        retry_total: int = 5,
        **kwargs,
    ):
        """Initialize FW async client."""
        self._cache: t.Dict[str, t.Tuple[t.Any, float]] = {}
        self.defer_auth = defer_auth
        self.drone_secret = drone_secret
        self.device_type = device_type
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
        # require device_label and default device_type to client_name if drone
        elif not api_key and self.drone_secret:
            if not self.device_label:  # pragma: no cover
                raise ValidationError("device_label required")
            if not self.device_type:
                self.device_type = client_name
        headers.setdefault("X-Accept-Feature", "Safe-Redirect")
        headers["User-Agent"] = dump_useragent(
            client_name,
            client_version,
            **client_info,
        )
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

    def prepare_request(self, url, opts):
        """Prepare request url and headers."""
        if not url.startswith("http"):
            svc_prefix = re.sub(r"^(/[^/]+)?.*$", r"\1", url)
            # use service base url if defined
            if self.svc_urls.get(svc_prefix):
                url = f"{self.svc_urls[svc_prefix]}{url}"
            # otherwise default to self.baseurl IFF looks like a domain
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
        # set authorization header from simple str auth kwarg
        if isinstance(opts.get("auth"), str):
            headers = opts.get("headers") or {}
            headers["Authorization"] = opts.pop("auth")
            opts["headers"] = headers
        return url, opts
