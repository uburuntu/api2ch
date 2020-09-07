import asyncio
from pathlib import Path

from api2ch.api import Api2chAsync
from api2ch.config import downloads_dir
from api2ch.models.file import File
from api2ch.utils import parse_url, prettify_bytes


def download_thread_media(url: str, path: Path = downloads_dir, with_thumbnails: bool = False, skip_if_exists: bool = True):
    valid, board, thread_id = parse_url(url)

    if not valid:
        return

    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        path = path.parent
    path = path / f'{board}_{thread_id}'
    path.mkdir(parents=True, exist_ok=True)

    async def download(concurrent_downloads: int = 10):
        s = asyncio.Semaphore(concurrent_downloads)

        async def download_single(file: File):
            async with s:
                size_ = await file.download_async(path, skip_if_exists)
                if with_thumbnails:
                    size_ += await file.download_thumbnail_async(path, skip_if_exists)
                return size_

        async with Api2chAsync() as api:
            t = await api.thread(board, thread_id)

            coros = []
            for p in t.posts:
                for f in p.files:
                    coros.append(download_single(f))

            return await asyncio.gather(*coros)

    loop = asyncio.get_event_loop()
    size = sum(loop.run_until_complete(download()))
    return prettify_bytes(size)
