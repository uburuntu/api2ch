from pathlib import Path
from typing import Optional

import aiofiles
import aiohttp
import requests
from pydantic import validator

from api2ch.config import API_BASE, downloads_dir
from api2ch.models.base import Base
from api2ch.utils import prettify_bytes


class File(Base):
    name: str
    type: int
    height: int
    width: int
    path: str
    size: int
    thumbnail: str
    tn_height: int
    tn_width: int

    @property
    def size_bytes(self) -> int:
        return self.size * 1024

    @property
    def size_string(self) -> str:
        return prettify_bytes(self.size_bytes)

    @property
    def original_name(self) -> str:
        return self.name

    @property
    def extension(self) -> str:
        if '.' not in self.name:
            return ''
        return self.name.lower().split('.')[-1]

    def url(self) -> str:
        return f'{API_BASE}{self.path}'

    def url_thumbnail(self) -> str:
        return f'{API_BASE}{self.thumbnail}'

    @staticmethod
    def _download_path(path: Path = None) -> Path:
        if path is None:
            path = downloads_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    async def _download_async(url: str, path: Path) -> int:
        chunk_size = 2 ** 14

        size = 0
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                async with aiofiles.open(str(path.absolute()), 'wb') as f:
                    while True:
                        chunk = await r.content.read(chunk_size)
                        if not chunk:
                            break
                        size += await f.write(chunk)
        return size

    async def download_async(self, path: Path = None, skip_if_exists: bool = True) -> int:
        path = self._download_path(path)
        if path.is_dir():
            prefix = self.name.split('.')[0]
            path = path / f'{prefix}_{self.original_name}'
        if skip_if_exists:
            if path.exists():
                return path.stat().st_size
        return await self._download_async(self.url(), path)

    async def download_thumbnail_async(self, path: Path = None, skip_if_exists: bool = True) -> int:
        path = self._download_path(path)
        if path.is_dir():
            filename = self.thumbnail.split('/')[-1]
            path = path / filename
        if skip_if_exists:
            if path.exists():
                return path.stat().st_size
        return await self._download_async(self.url_thumbnail(), path)

    @staticmethod
    def _download(url: str, path: Path) -> int:
        chunk_size = 2 ** 14

        size = 0
        with requests.get(url, stream=True, timeout=5 * 60) as r:
            with path.open('wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    size += f.write(chunk)
        return size

    def download(self, path: Path = None, skip_if_exists: bool = True) -> int:
        path = self._download_path(path)
        if path.is_dir():
            prefix = self.name.split('.')[0]
            path = path / f'{prefix}_{self.original_name}'
        if skip_if_exists:
            if path.exists():
                return path.stat().st_size
        return self._download(self.url(), path)

    def download_thumbnail(self, path: Path = None, skip_if_exists: bool = True) -> int:
        path = self._download_path(path)
        if path.is_dir():
            filename = self.thumbnail.split('/')[-1]
            path = path / filename
        if skip_if_exists:
            if path.exists():
                return path.stat().st_size
        return self._download(self.url_thumbnail(), path)


class Image(File):
    fullname: str
    displayname: str
    md5: str
    nsfw: bool

    @property
    def original_name(self) -> str:
        return self.fullname

    @validator('type')
    def type_check(cls, v):
        assert v in (1, 2, 4)
        return v


class Video(File):
    fullname: str
    displayname: str
    md5: str
    nsfw: bool
    duration: Optional[str]
    duration_secs: Optional[str]

    @property
    def original_name(self) -> str:
        return self.fullname

    @validator('type')
    def type_check(cls, v):
        assert v in (6, 10)
        return v


class Sticker(File):
    install: str
    pack: str
    sticker: str

    @validator('type')
    def type_check(cls, v):
        assert v in (100,)
        return v
