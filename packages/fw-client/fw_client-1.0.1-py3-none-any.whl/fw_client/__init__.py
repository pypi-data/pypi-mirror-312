"""Flywheel HTTP API Client."""

from . import errors
from .async_client import FWClientAsync
from .client import FWClient
from .errors import (
    ClientError,
    Conflict,
    ConnectError,
    HTTPStatusError,
    NotFound,
    ServerError,
    ValidationError,
)

__all__ = [
    "ClientError",
    "Conflict",
    "ConnectError",
    "FWClient",
    "FWClientAsync",
    "HTTPStatusError",
    "NotFound",
    "ServerError",
    "ValidationError",
]


setattr(HTTPStatusError, "__str__", errors.http_error_str)
