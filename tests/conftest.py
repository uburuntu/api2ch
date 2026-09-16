import copy
import json
from pathlib import Path

import httpx
import pytest
import pytest_asyncio

from api2ch import Api2ch, Api2chAsync


@pytest.fixture(scope="session")
def wire() -> dict:
    path = Path(__file__).parent / "fixtures" / "current_api.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def handler(wire: dict):
    board = wire["board"]
    post = wire["post"]
    summary = wire["summary"]
    post_with_file = copy.deepcopy(post)
    post_with_file["files"] = [wire["file"]]

    def response(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        routes = {
            "/api/mobile/v2/boards": [board],
            "/pr/threads.json": {"board": "pr", "threads": [summary]},
            "/pr/catalog.json": {
                "board": board,
                "filter": "date",
                "threads": [post_with_file],
            },
            "/pr/catalog_num.json": {"board": board, "filter": "num", "threads": [post]},
            "/pr/index.json": {
                "board": board,
                "board_speed": 1,
                "current_page": 0,
                "current_thread": 0,
                "is_board": True,
                "is_index": True,
                "pages": [0],
                "threads": [
                    {"thread_num": 100, "files_count": 0, "posts_count": 1, "posts": [post]}
                ],
            },
            "/pr/res/100.json": {
                "board": board,
                "current_thread": 100,
                "files_count": 0,
                "is_board": False,
                "is_closed": 0,
                "is_index": False,
                "max_num": 100,
                "posts_count": 1,
                "thread_first_image": "",
                "threads": [{"posts": [post]}],
                "title": "Fixture subject",
                "unique_posters": 1,
            },
            "/api/mobile/v2/info/pr/100": {
                "result": 1,
                "thread": {"num": 100, "timestamp": 1700000000, "posts": 1},
            },
            "/api/mobile/v2/after/pr/100/100": {"result": 1, "unique_posters": 1, "posts": [post]},
            "/api/mobile/v2/post/pr/100": {"result": 1, "post": post},
            "/missing": {"result": 0, "error": {"code": -3, "message": "Thread is gone"}},
            "/bad-schema": {"board": 7},
        }
        if path == "/malformed":
            return httpx.Response(200, content=b"not json", request=request)
        if path == "/http-error":
            return httpx.Response(503, request=request)
        payload = routes.get(path)
        if payload is None:
            return httpx.Response(404, request=request)
        return httpx.Response(200, json=copy.deepcopy(payload), request=request)

    return response


@pytest.fixture
def api(handler):
    client = httpx.Client(transport=httpx.MockTransport(handler))
    with client, Api2ch(client=client) as value:
        yield value


@pytest_asyncio.fixture
async def api_async(handler):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    async with client, Api2chAsync(client=client) as value:
        yield value
