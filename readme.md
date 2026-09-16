# api2ch

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/api2ch.svg)](https://pypi.org/project/api2ch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![Python Tests](https://github.com/uburuntu/api2ch/actions/workflows/tests.yml/badge.svg)](https://github.com/uburuntu/api2ch/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/uburuntu/api2ch/branch/master/graph/badge.svg)](https://codecov.io/gh/uburuntu/api2ch)

⚡ Typed synchronous and asynchronous clients for the read-only 2ch API.

Version 2 uses the current `/api/mobile/v2` endpoints, HTTPX and native Pydantic 2 models. It requires Python 3.14 or newer.

## 🎒 Installation

```console
pip install api2ch
```

## 🛠 Examples

### Synchronous

```python
from api2ch import Api2ch

with Api2ch() as api:
    boards = api.boards()
    threads = api.threads("pr")

    for thread in threads.sorted_by_views()[:3]:
        print(thread.num, thread.header, thread.views)
```

### Asynchronous

```python
import asyncio

from api2ch import Api2chAsync


async def main() -> None:
    async with Api2chAsync() as api:
        threads = await api.threads("hw")
        thread = await api.thread("hw", threads.threads[0].num)
        print(thread.posts[0].body_text)


asyncio.run(main())
```

### Current mobile API

```python
with Api2ch() as api:
    thread_id = api.threads("pr").threads[0].num
    info = api.thread_info("pr", thread_id)
    new_posts = api.posts_after("pr", thread_id, thread_id)
    opening_post = api.post("pr", thread_id)
```

`boards_by_types()` now returns a dynamic `dict[str, list[Board]]`; categories are no longer fixed translated attributes.

### Raw JSON

Typed calls never fall back to unvalidated data. Use the explicit raw namespace when the original JSON is needed:

```python
with Api2ch() as api:
    payload = api.raw.catalog("pr")
```

The raw namespace still applies timeout, transport, HTTP, JSON and upstream error handling.

## 📜 Methods

| Method | Current route |
|---|---|
| `boards()` | `/api/mobile/v2/boards` |
| `threads(board)` | `/{board}/threads.json` |
| `catalog(board)` | `/{board}/catalog.json` |
| `catalog_by_date(board)` | `/{board}/catalog_num.json` |
| `page(board, page)` | `/{board}/{page}.json` |
| `thread(board, thread)` | `/{board}/res/{thread}.json` |
| `thread_info(board, thread)` | `/api/mobile/v2/info/{board}/{thread}` |
| `posts_after(board, thread, num)` | `/api/mobile/v2/after/{board}/{thread}/{num}` |
| `post(board, num)` | `/api/mobile/v2/post/{board}/{num}` |

`thread_posts_by_num` and `single_post` remain as unambiguous compatibility aliases. The removed ordinal-based `thread_posts_by_post` endpoint has no current upstream equivalent.

## ⚠ Errors and ownership

`Api2chError` has distinct subclasses for timeouts, transport failures, HTTP status failures, upstream error envelopes, malformed JSON and response validation. Error objects retain the URL and, where applicable, an HTTP or upstream error code.

Clients created by api2ch are closed by their context manager. An injected `httpx.Client` or `httpx.AsyncClient` remains owned by the caller.

## 🧪 Development

```console
uv sync --locked --extra dev
uv run ruff format --check api2ch tests
uv run ruff check api2ch tests
uv run mypy api2ch
uv run pytest -m "not integration"
```

The ordinary suite is deterministic and offline. Maintainers can run the small read-only live contract suite with `uv run pytest tests/test_integration.py -v`, or through the manual GitHub Actions input.

See the [verified upstream contract](docs/api-contract.md), [2.0 migration guide](docs/migration-2.md), and [release procedure](RELEASING.md).

## 📝 License

[MIT](LICENSE)
