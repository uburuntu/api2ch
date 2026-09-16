"""Typed synchronous and asynchronous clients for the read-only 2ch API."""

from api2ch.api import (
    Api2ch,
    Api2chAsync,
    Api2chError,
    Api2chHTTPError,
    Api2chResponseError,
    Api2chTimeoutError,
    Api2chTransportError,
    Api2chUpstreamError,
    Api2chValidationError,
)
from api2ch.config import API_BASE, api_mirrors, downloads_dir
from api2ch.downloads import DownloadResult, download_file, download_file_async
from api2ch.helpers import ThreadDownloadResult, download_thread_media
from api2ch.models import *  # noqa: F403
from api2ch.utils import clear_html, convert_html, parse_url, prettify_bytes

__author__ = "uburuntu"
__email__ = "github@rmbk.me"
__license__ = "MIT"
__version__ = "2.0.0"

__all__ = [
    "API_BASE",
    "Api2ch",
    "Api2chAsync",
    "Api2chError",
    "Api2chHTTPError",
    "Api2chResponseError",
    "Api2chTimeoutError",
    "Api2chTransportError",
    "Api2chUpstreamError",
    "Api2chValidationError",
    "DownloadResult",
    "ThreadDownloadResult",
    "api_mirrors",
    "clear_html",
    "convert_html",
    "download_file",
    "download_file_async",
    "download_thread_media",
    "downloads_dir",
    "parse_url",
    "prettify_bytes",
]
