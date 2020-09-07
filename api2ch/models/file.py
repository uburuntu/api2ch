from typing import Optional

from api2ch.models.base import Base


class File(Base):
    displayname: Optional[str]
    fullname: Optional[str] = None
    height: int
    md5: Optional[str] = None
    name: str
    nsfw: Optional[int] = None
    path: str
    size: int
    thumbnail: str
    tn_height: int
    tn_width: int
    type: int
    width: int
    duration: Optional[str] = None
    duration_secs: Optional[int] = None
    install: Optional[str] = None
    pack: Optional[str] = None
    sticker: Optional[str] = None
