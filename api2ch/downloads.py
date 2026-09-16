import os
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import anyio
import httpx

from api2ch.config import API_BASE, DEFAULT_TIMEOUT, downloads_dir
from api2ch.models.file import File


@dataclass(frozen=True, slots=True)
class DownloadResult:
    path: Path
    bytes_written: int
    skipped: bool = False


def _safe_name(value: str) -> str:
    name = PurePosixPath(value.replace("\\", "/")).name
    if name in {"", ".", ".."}:
        raise ValueError("remote file has no safe filename")
    return name


def _target(file: File, destination: str | Path | None) -> Path:
    if destination is None:
        destination = downloads_dir
    target = Path(destination)
    if (target.exists() and target.is_dir()) or (not target.exists() and not target.suffix):
        target = target / _safe_name(file.original_name)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def download_file(
    file: File,
    destination: str | Path | None = None,
    *,
    base_url: str = API_BASE,
    skip_if_exists: bool = True,
    client: httpx.Client | None = None,
) -> DownloadResult:
    target = _target(file, destination)
    if skip_if_exists and target.is_file():
        return DownloadResult(target, target.stat().st_size, skipped=True)

    own_client = client is None
    active_client = client or httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".part", dir=target.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    size = 0
    try:
        with active_client.stream("GET", file.url(base_url)) as response:
            response.raise_for_status()
            with temporary.open("wb") as stream:
                for chunk in response.iter_bytes():
                    size += stream.write(chunk)
        temporary.replace(target)
        return DownloadResult(target, size)
    finally:
        temporary.unlink(missing_ok=True)
        if own_client:
            active_client.close()


async def download_file_async(
    file: File,
    destination: str | Path | None = None,
    *,
    base_url: str = API_BASE,
    skip_if_exists: bool = True,
    client: httpx.AsyncClient | None = None,
) -> DownloadResult:
    target = _target(file, destination)
    if skip_if_exists and target.is_file():
        size = await anyio.to_thread.run_sync(lambda: target.stat().st_size)
        return DownloadResult(target, size, skipped=True)

    own_client = client is None
    active_client = client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".part", dir=target.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    size = 0
    try:
        async with active_client.stream("GET", file.url(base_url)) as response:
            response.raise_for_status()
            async with await anyio.open_file(temporary, "wb") as stream:
                async for chunk in response.aiter_bytes():
                    size += await stream.write(chunk)
        await anyio.to_thread.run_sync(temporary.replace, target)
        return DownloadResult(target, size)
    finally:
        await anyio.to_thread.run_sync(temporary.unlink, True)
        if own_client:
            await active_client.aclose()
