"""Flywheel client common helpers, constants."""

import platform
import re
from importlib.metadata import version as pkg_version

import httpx
from fw_utils import attrify
from httpx._auth import FunctionAuth

from .errors import ClientError, Conflict, NotFound, ServerError

# regex to match api keys with (to extract the host if it's embedded)
API_KEY_RE = re.compile(
    r"(?i)"
    r"((?P<api_key_type>bearer|scitran-user) )?"
    r"((?P<scheme>https?://)?(?P<host>[^:]+)(?P<port>:\d+)?:)?"
    r"(?P<api_key>.+)"
)
MEGABYTE = 1 << 20
# cache time to live (duration to cache /api/config and /api/version response)
CACHE_TTL = 3600  # 1 hour
# x-accept-feature header sent by default to core-api
CORE_FEATURES = (
    "multipart_signed_url",
    "pagination",
    "safe-redirect",
    "subject-container",
)

# global cache of drone keys (device api keys acquired via drone secret)
DRONE_DEVICE_KEYS = {}
# retry
RETRY_METHODS = ("DELETE", "GET", "HEAD", "POST", "PUT", "OPTIONS")
RETRY_STATUSES = (429, 502, 503, 504)


class Response(httpx.Response):
    """Response with attrified JSONs.

    Changes:
      json()             - Return data attrified (dict keys are attr-accessible)
      raise_for_status() - Raise distinct HTTP errors for 4xx / 5xx statuses
    """

    def json(self, **kwargs):
        """Return loaded JSON response with attribute access enabled."""
        return attrify(super().json(**kwargs))

    def raise_for_status(self) -> httpx.Response:
        """Raise ClientError for 4xx / ServerError for 5xx responses."""
        try:
            return super().raise_for_status()
        except httpx.HTTPStatusError as exc:
            if self.status_code == 404:
                exc.__class__ = NotFound  # pragma: no cover
            elif self.status_code == 409:
                exc.__class__ = Conflict  # pragma: no cover
            elif self.status_code < 500:
                exc.__class__ = ClientError
            else:
                exc.__class__ = ServerError
            raise


def dump_useragent(*args: str, **kwargs: str) -> str:
    """Return parsable UA string for the given agent info."""
    useragent = f"fw-client/{pkg_version('fw_client')}"
    kwargs = {"platform": platform.platform()} | kwargs
    comments = list(args) + [f"{k}:{v}" if v else k for k, v in kwargs.items()]
    return f"{useragent} ({'; '.join(comments)})"


def httpx_pop_auth_header(request):
    """Pop authorization header from request to enable anonymous request."""
    request.headers.pop("Authorization", None)
    return request


httpx_anon = FunctionAuth(httpx_pop_auth_header)
