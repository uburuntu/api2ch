import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

import httpx
from pydantic import TypeAdapter, ValidationError
from typing_extensions import TypeForm

from api2ch.config import API_BASE, DEFAULT_TIMEOUT, USER_AGENT
from api2ch.models.auxiliary import ThreadInfo
from api2ch.models.board import Board
from api2ch.models.post import Post
from api2ch.models.response import (
    ResponseCatalog,
    ResponsePage,
    ResponseSinglePost,
    ResponseThread,
    ResponseThreadInfo,
    ResponseThreadPostsByNum,
    ResponseThreads,
)

Json = dict[str, Any] | list[Any] | str | int | float | bool | None
_BOARD = re.compile(r"[a-z0-9_]+")


class Api2chError(Exception):
    def __init__(self, message: str, *, code: int | None = None, url: str | None = None):
        super().__init__(message)
        self.code = code
        self.reason = message
        self.url = url

    def __repr__(self) -> str:
        prefix = f"[{self.code}] " if self.code is not None else ""
        return f"{type(self).__name__}({prefix}{self.reason})"


class Api2chTransportError(Api2chError):
    pass


class Api2chTimeoutError(Api2chTransportError):
    pass


class Api2chHTTPError(Api2chError):
    pass


class Api2chUpstreamError(Api2chError):
    pass


class Api2chResponseError(Api2chError):
    pass


class Api2chValidationError(Api2chResponseError):
    pass


def _board(value: str) -> str:
    if _BOARD.fullmatch(value) is None:
        raise ValueError(f"invalid board id: {value!r}")
    return value


def _positive(value: str | int, name: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a positive integer") from error
    if parsed < 1:
        raise ValueError(f"{name} must be a positive integer")
    return parsed


def _page(value: str | int) -> str:
    if value == "index":
        return "index"
    parsed = int(value)
    if parsed < 0:
        raise ValueError("page must be 'index' or a non-negative integer")
    return str(parsed)


def _decode(response: httpx.Response) -> Json:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise Api2chHTTPError(
            f"upstream returned HTTP {response.status_code}",
            code=response.status_code,
            url=str(response.url),
        ) from error
    try:
        result: Json = response.json()
    except ValueError as error:
        raise Api2chResponseError(
            "upstream returned malformed JSON", url=str(response.url)
        ) from error
    if isinstance(result, Mapping) and result.get("result") == 0:
        details = result.get("error")
        if isinstance(details, Mapping):
            code = details.get("code")
            message = details.get("message", "upstream request failed")
            raise Api2chUpstreamError(
                str(message),
                code=code if isinstance(code, int) else None,
                url=str(response.url),
            )
        raise Api2chUpstreamError("upstream request failed", url=str(response.url))
    return result


def _validate[T](data: Json, expected: TypeForm[T], url: str) -> T:
    try:
        return TypeAdapter(expected).validate_python(data)
    except ValidationError as error:
        raise Api2chValidationError(
            "upstream response did not match the expected schema", url=url
        ) from error


class Api2chBase:
    def __init__(self, *, base_url: str = API_BASE) -> None:
        self.api_base = self._normalize_base_url(base_url)

    @staticmethod
    def _normalize_base_url(value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) origin")
        return value.rstrip("/")

    def set_api_base(self, api_base: str) -> Api2chBase:
        self.api_base = self._normalize_base_url(api_base)
        return self

    def reset_api_base(self) -> Api2chBase:
        self.api_base = API_BASE
        return self

    def _url(self, path: str) -> str:
        return f"{self.api_base}/{path.lstrip('/')}"


class _RawSync:
    def __init__(self, api: Api2ch) -> None:
        self._api = api

    def get(self, path: str) -> Json:
        return self._api._get_json(path)

    def boards(self) -> Json:
        return self.get("/api/mobile/v2/boards")

    def thread(self, board: str, thread: str | int) -> Json:
        return self.get(f"/{_board(board)}/res/{_positive(thread, 'thread')}.json")

    def threads(self, board: str) -> Json:
        return self.get(f"/{_board(board)}/threads.json")

    def catalog(self, board: str) -> Json:
        return self.get(f"/{_board(board)}/catalog.json")

    def catalog_by_date(self, board: str) -> Json:
        return self.get(f"/{_board(board)}/catalog_num.json")

    def page(self, board: str, page: str | int = "index") -> Json:
        return self.get(f"/{_board(board)}/{_page(page)}.json")

    def thread_info(self, board: str, thread: str | int) -> Json:
        return self.get(f"/api/mobile/v2/info/{_board(board)}/{_positive(thread, 'thread')}")

    def posts_after(self, board: str, thread: str | int, num: str | int) -> Json:
        return self.get(
            f"/api/mobile/v2/after/{_board(board)}/{_positive(thread, 'thread')}/"
            f"{_positive(num, 'num')}"
        )

    def post(self, board: str, num: str | int) -> Json:
        return self.get(f"/api/mobile/v2/post/{_board(board)}/{_positive(num, 'num')}")


class Api2ch(Api2chBase):
    def __init__(
        self,
        *,
        base_url: str = API_BASE,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(base_url=base_url)
        self._timeout = timeout
        self._headers = {"User-Agent": USER_AGENT, **(headers or {})}
        self._client = client
        self._owns_client = client is None
        self._closed = False
        self.raw = _RawSync(self)

    @property
    def client(self) -> httpx.Client:
        if self._closed:
            raise RuntimeError("client is closed")
        if self._client is None:
            self._client = httpx.Client(
                timeout=self._timeout,
                headers=self._headers,
                follow_redirects=True,
            )
        return self._client

    def close(self) -> None:
        if not self._closed and self._owns_client and self._client is not None:
            self._client.close()
        self._closed = True

    def __enter__(self) -> Api2ch:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _get_json(self, path: str) -> Json:
        url = self._url(path)
        try:
            return _decode(self.client.get(url))
        except httpx.TimeoutException as error:
            raise Api2chTimeoutError("upstream request timed out", url=url) from error
        except httpx.TransportError as error:
            raise Api2chTransportError("upstream transport failed", url=url) from error

    def _get[T](self, path: str, expected: TypeForm[T]) -> T:
        url = self._url(path)
        return _validate(self._get_json(path), expected, url)

    def boards(self) -> list[Board]:
        return self._get("/api/mobile/v2/boards", list[Board])

    def boards_by_types(self) -> dict[str, list[Board]]:
        result: dict[str, list[Board]] = {}
        for board in self.boards():
            result.setdefault(board.category, []).append(board)
        return result

    def thread(self, board: str, thread: str | int) -> ResponseThread:
        return self._get(f"/{_board(board)}/res/{_positive(thread, 'thread')}.json", ResponseThread)

    def threads(self, board: str) -> ResponseThreads:
        return self._get(f"/{_board(board)}/threads.json", ResponseThreads)

    def catalog(self, board: str) -> ResponseCatalog:
        return self._get(f"/{_board(board)}/catalog.json", ResponseCatalog)

    def catalog_by_date(self, board: str) -> ResponseCatalog:
        return self._get(f"/{_board(board)}/catalog_num.json", ResponseCatalog)

    def page(self, board: str, page: str | int = "index") -> ResponsePage:
        return self._get(f"/{_board(board)}/{_page(page)}.json", ResponsePage)

    def thread_info(self, board: str, thread: str | int) -> ThreadInfo:
        response = self._get(
            f"/api/mobile/v2/info/{_board(board)}/{_positive(thread, 'thread')}",
            ResponseThreadInfo,
        )
        if response.thread is None:
            raise Api2chResponseError("upstream response omitted thread information")
        return response.thread

    def posts_after(
        self, board: str, thread: str | int, num: str | int
    ) -> ResponseThreadPostsByNum:
        return self._get(
            f"/api/mobile/v2/after/{_board(board)}/"
            f"{_positive(thread, 'thread')}/{_positive(num, 'num')}",
            ResponseThreadPostsByNum,
        )

    def post(self, board: str, num: str | int) -> Post:
        response = self._get(
            f"/api/mobile/v2/post/{_board(board)}/{_positive(num, 'num')}",
            ResponseSinglePost,
        )
        if response.post is None:
            raise Api2chResponseError("upstream response omitted the post")
        return response.post

    thread_posts_by_num = posts_after
    single_post = post


class _RawAsync:
    def __init__(self, api: Api2chAsync) -> None:
        self._api = api

    async def get(self, path: str) -> Json:
        return await self._api._get_json(path)

    async def boards(self) -> Json:
        return await self.get("/api/mobile/v2/boards")

    async def thread(self, board: str, thread: str | int) -> Json:
        return await self.get(f"/{_board(board)}/res/{_positive(thread, 'thread')}.json")

    async def threads(self, board: str) -> Json:
        return await self.get(f"/{_board(board)}/threads.json")

    async def catalog(self, board: str) -> Json:
        return await self.get(f"/{_board(board)}/catalog.json")

    async def catalog_by_date(self, board: str) -> Json:
        return await self.get(f"/{_board(board)}/catalog_num.json")

    async def page(self, board: str, page: str | int = "index") -> Json:
        return await self.get(f"/{_board(board)}/{_page(page)}.json")

    async def thread_info(self, board: str, thread: str | int) -> Json:
        return await self.get(f"/api/mobile/v2/info/{_board(board)}/{_positive(thread, 'thread')}")

    async def posts_after(self, board: str, thread: str | int, num: str | int) -> Json:
        return await self.get(
            f"/api/mobile/v2/after/{_board(board)}/{_positive(thread, 'thread')}/"
            f"{_positive(num, 'num')}"
        )

    async def post(self, board: str, num: str | int) -> Json:
        return await self.get(f"/api/mobile/v2/post/{_board(board)}/{_positive(num, 'num')}")


class Api2chAsync(Api2chBase):
    def __init__(
        self,
        *,
        base_url: str = API_BASE,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(base_url=base_url)
        self._timeout = timeout
        self._headers = {"User-Agent": USER_AGENT, **(headers or {})}
        self._client = client
        self._owns_client = client is None
        self._closed = False
        self.raw = _RawAsync(self)

    @property
    def client(self) -> httpx.AsyncClient:
        if self._closed:
            raise RuntimeError("client is closed")
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self._timeout,
                headers=self._headers,
                follow_redirects=True,
            )
        return self._client

    async def close(self) -> None:
        if not self._closed and self._owns_client and self._client is not None:
            await self._client.aclose()
        self._closed = True

    async def __aenter__(self) -> Api2chAsync:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def _get_json(self, path: str) -> Json:
        url = self._url(path)
        try:
            return _decode(await self.client.get(url))
        except httpx.TimeoutException as error:
            raise Api2chTimeoutError("upstream request timed out", url=url) from error
        except httpx.TransportError as error:
            raise Api2chTransportError("upstream transport failed", url=url) from error

    async def _get[T](self, path: str, expected: TypeForm[T]) -> T:
        url = self._url(path)
        return _validate(await self._get_json(path), expected, url)

    async def boards(self) -> list[Board]:
        return await self._get("/api/mobile/v2/boards", list[Board])

    async def boards_by_types(self) -> dict[str, list[Board]]:
        result: dict[str, list[Board]] = {}
        for board in await self.boards():
            result.setdefault(board.category, []).append(board)
        return result

    async def thread(self, board: str, thread: str | int) -> ResponseThread:
        return await self._get(
            f"/{_board(board)}/res/{_positive(thread, 'thread')}.json", ResponseThread
        )

    async def threads(self, board: str) -> ResponseThreads:
        return await self._get(f"/{_board(board)}/threads.json", ResponseThreads)

    async def catalog(self, board: str) -> ResponseCatalog:
        return await self._get(f"/{_board(board)}/catalog.json", ResponseCatalog)

    async def catalog_by_date(self, board: str) -> ResponseCatalog:
        return await self._get(f"/{_board(board)}/catalog_num.json", ResponseCatalog)

    async def page(self, board: str, page: str | int = "index") -> ResponsePage:
        return await self._get(f"/{_board(board)}/{_page(page)}.json", ResponsePage)

    async def thread_info(self, board: str, thread: str | int) -> ThreadInfo:
        response = await self._get(
            f"/api/mobile/v2/info/{_board(board)}/{_positive(thread, 'thread')}",
            ResponseThreadInfo,
        )
        if response.thread is None:
            raise Api2chResponseError("upstream response omitted thread information")
        return response.thread

    async def posts_after(
        self, board: str, thread: str | int, num: str | int
    ) -> ResponseThreadPostsByNum:
        return await self._get(
            f"/api/mobile/v2/after/{_board(board)}/"
            f"{_positive(thread, 'thread')}/{_positive(num, 'num')}",
            ResponseThreadPostsByNum,
        )

    async def post(self, board: str, num: str | int) -> Post:
        response = await self._get(
            f"/api/mobile/v2/post/{_board(board)}/{_positive(num, 'num')}",
            ResponseSinglePost,
        )
        if response.post is None:
            raise Api2chResponseError("upstream response omitted the post")
        return response.post

    thread_posts_by_num = posts_after
    single_post = post
