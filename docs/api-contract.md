# Verified upstream contract

Verified on 16 September 2026 against `https://2ch.su` with read-only requests.

The official [API guide](https://2ch.su/abu/res/42375.html) links [OpenAPI 1.0.31](https://2ch.su/api.yml). The retrieved document had SHA-256 `9d8ced595f2d089e29d61a975677b263f4b0c93307b82c599b9a373382426e55` and a server `Last-Modified` value of 31 August 2024.

## Endpoint matrix

| Capability | Route | Observed result | 2.0 decision |
|---|---|---|---|
| Boards | `/api/mobile/v2/boards` | JSON array of board objects | Use |
| Thread summaries | `/{board}/threads.json` | Object with `board` and `threads` | Keep |
| Catalog, activity order | `/{board}/catalog.json` | Object with nested `board` and OP posts | Keep |
| Catalog, creation order | `/{board}/catalog_num.json` | Same envelope as catalog | Keep |
| Board page | `/{board}/{page}.json` | Nested `board`; threads contain posts | Keep |
| Complete thread | `/{board}/res/{thread}.json` | Nested `board`; one thread containing posts | Keep |
| Thread information | `/api/mobile/v2/info/{board}/{thread}` | `result` plus `thread` | Add |
| Posts at or after a board post number | `/api/mobile/v2/after/{board}/{thread}/{num}` | `result`, `unique_posters`, `posts` | Replaces legacy `get_thread&num=` |
| Single post | `/api/mobile/v2/post/{board}/{num}` | `result` plus `post` | Replaces legacy `get_post` |
| Legacy boards | `/boards.json` | HTTP 404 | Remove |
| Legacy mobile reads | `/makaba/mobile.fcgi?...` | HTTP 404 | Remove |
| Posts after a thread ordinal | Legacy `get_thread&post=` | No documented v2 equivalent | Unsupported |

The v2 mobile API reports missing boards, threads and posts as an HTTP 200 JSON error envelope with `result: 0` and an `error` object. The client converts that envelope to `Api2chUpstreamError`.

Observed compatibility details covered by fixtures and live tests:

- board metadata is a nested object in catalog, page and thread responses;
- page post entries may contain `files: null`, normalized to an empty list;
- incidental presentation fields may be absent;
- unknown response fields and unknown numeric attachment types are preserved;
- mobile boards are a flat array, so categories are grouped dynamically client-side.

Fixtures in `tests/fixtures/current_api.json` contain synthetic text and identifiers, not copied user media or post content. `tests/test_integration.py` discovers a current thread at runtime instead of depending on a historical thread remaining available.
