# Migrating from api2ch 1.x

api2ch 2.0 is a deliberate breaking release for Python 3.14 and the current upstream API.

## Runtime and lifecycle

- Python 3.14 or newer is required.
- Requests, aiohttp and aiofiles were replaced by HTTPX and AnyIO.
- Use `Api2ch` or `Api2chAsync` as a context manager. Injected HTTPX clients remain caller-owned.
- `raw_results=True` was removed. Use `api.raw.<method>(...)` explicitly.

## Endpoint changes

- `boards()` now reads `/api/mobile/v2/boards` and returns `list[Board]`.
- `boards_by_types()` returns a dynamic dictionary keyed by the upstream category text.
- `thread_info()`, `posts_after()` and `post()` expose the current mobile v2 API.
- `thread_posts_by_num` aliases `posts_after`; `single_post` aliases `post`.
- `thread_posts_by_post` was removed because the ordinal-based legacy operation has no documented v2 equivalent.
- API errors inside HTTP 200 responses now raise `Api2chUpstreamError`.

## Models and exports

- Models use native Pydantic 2 APIs such as `model_validate()` and `model_dump()`.
- Requests no longer execute themselves and responses no longer retain a live request/client reference.
- `Request*`, `Response`, `NewsAbu`, `Top` and `Tag` are no longer public API.
- Board metadata is available through `response.board`, for example `response.board.name`.
- Board categories are not translated into fixed attributes.
- Model methods no longer download data. Use `download_file()` or `download_file_async()`.

## Downloads

Downloads check HTTP status, stream to a temporary file and atomically replace the destination after success. They return `DownloadResult` with the destination, transferred byte count and skip status. A destination with a suffix is treated as a filename; an existing directory or suffixless new path is treated as a directory.
