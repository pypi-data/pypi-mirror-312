"""Flywheel HTTP API Client."""

from . import errors
from .async_client import FWClientAsync
from .client import FWClient
from .errors import (
    ClientError,
    Conflict,
    HTTPStatusError,
    NotFound,
    ServerError,
    ValidationError,
)

__all__ = [
    "ClientError",
    "Conflict",
    "ConnectionError",
    "FWClient",
    "FWClientAsync",
    "HTTPStatusError",
    "NotFound",
    "ServerError",
    "ValidationError",
]


setattr(HTTPStatusError, "__str__", errors.http_error_str)
