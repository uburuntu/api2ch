from enum import IntEnum
from pathlib import PurePosixPath

from api2ch.config import API_BASE
from api2ch.models.base import Base
from api2ch.utils import prettify_bytes


class FileType(IntEnum):
    none = 0
    jpeg = 1
    png = 2
    apng = 3
    gif = 4
    bmp = 5
    webm = 6
    mp3 = 7
    ogg = 8
    mp4 = 10
    sticker = 100


class File(Base):
    name: str
    path: str
    thumbnail: str
    type: int
    size: int
    width: int
    height: int
    tn_width: int
    tn_height: int
    fullname: str | None = None
    displayname: str | None = None
    md5: str | None = None
    nsfw: int | None = None
    duration: str | None = None
    duration_secs: int | None = None
    pack: str | None = None
    sticker: str | None = None
    install: str | None = None

    @property
    def size_bytes(self) -> int:
        return self.size * 1024

    @property
    def size_string(self) -> str:
        return prettify_bytes(self.size_bytes)

    @property
    def original_name(self) -> str:
        return self.fullname or self.displayname or self.name

    @property
    def extension(self) -> str:
        return PurePosixPath(self.name).suffix.removeprefix(".").lower()

    def url(self, base_url: str = API_BASE) -> str:
        return f"{base_url.rstrip('/')}/{self.path.lstrip('/')}"

    def url_thumbnail(self, base_url: str = API_BASE) -> str:
        return f"{base_url.rstrip('/')}/{self.thumbnail.lstrip('/')}"


Image = File
Video = File
Sticker = File
