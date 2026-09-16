from pathlib import Path

import httpx
import pytest

from api2ch import download_file, download_file_async
from api2ch.models.file import File


def _file() -> File:
    return File(
        name="100.png",
        fullname="../safe.png",
        path="/pr/src/100.png",
        thumbnail="/pr/thumb/100s.png",
        type=1,
        size=1,
        width=1,
        height=1,
        tn_width=1,
        tn_height=1,
    )


def test_sync_download_is_atomic_and_skippable(tmp_path: Path) -> None:
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, content=b"data"))
    )
    with client:
        first = download_file(_file(), tmp_path, client=client)
        second = download_file(_file(), tmp_path, client=client)
    assert first.path == tmp_path / "safe.png"
    assert first.path.read_bytes() == b"data"
    assert second.skipped is True
    assert not list(tmp_path.glob("*.part"))


@pytest.mark.asyncio
async def test_async_download(tmp_path: Path) -> None:
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, content=b"async"))
    )
    async with client:
        result = await download_file_async(_file(), tmp_path / "named.bin", client=client)
    assert result.path.read_bytes() == b"async"
