import datetime
from typing import List, Optional, Union

from api2ch.config import API_BASE
from api2ch.models.base import Base
from api2ch.models.file import File, Image, Sticker, Video


class Post(Base):
    subject: str
    comment: str
    files: List[Union[Image, Video, Sticker, File]]
    timestamp: int
    date: str

    def dt(self, tz=None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp, tz=tz)

    lasthit: int

    def dt_last_post(self, tz=None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.lasthit, tz=tz)

    num: int
    parent: int

    @property
    def post_id(self) -> int:
        return self.num

    @property
    def parent_id(self) -> int:
        return self.parent or self.num

    def url(self, board: str):
        return f'{API_BASE}/{board}/res/{self.parent_id}.html#{self.post_id}'

    banned: bool
    closed: bool
    op: bool
    endless: bool
    sticky: int

    email: str
    name: str
    trip: str

    number: Optional[int]
    tags: Optional[str]
    trip_type: Optional[str]
    unique_posters: Optional[str]
    files_count: Optional[int]
    posts_count: Optional[int]
