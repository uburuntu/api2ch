from dataclasses import dataclass
from pathlib import Path

from api2ch.api import Api2ch
from api2ch.config import downloads_dir
from api2ch.downloads import DownloadResult, download_file
from api2ch.utils import parse_url


@dataclass(frozen=True, slots=True)
class ThreadDownloadResult:
    files: tuple[DownloadResult, ...]

    @property
    def bytes_written(self) -> int:
        return sum(item.bytes_written for item in self.files if not item.skipped)


def download_thread_media(
    url: str,
    path: Path = downloads_dir,
    *,
    skip_if_exists: bool = True,
) -> ThreadDownloadResult:
    valid, board, thread_id = parse_url(url)
    if not valid:
        raise ValueError("url is not a valid 2ch thread URL")

    destination = path / f"{board}_{thread_id}"
    results: list[DownloadResult] = []
    with Api2ch() as api:
        response = api.thread(board, thread_id)
        for post in response.posts:
            for file in post.files:
                results.append(
                    download_file(
                        file,
                        destination,
                        base_url=api.api_base,
                        skip_if_exists=skip_if_exists,
                        client=api.client,
                    )
                )
    return ThreadDownloadResult(tuple(results))
