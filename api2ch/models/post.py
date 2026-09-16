import datetime

from pydantic import Field, field_validator

from api2ch.config import API_BASE
from api2ch.models.auxiliary import BannedStatus
from api2ch.models.base import Base
from api2ch.models.file import File
from api2ch.utils import clear_html, convert_html


class Post(Base):
    num: int
    parent: int
    board: str
    timestamp: int
    lasthit: int
    date: str
    comment: str
    views: int
    sticky: int
    endless: int
    closed: int
    banned: BannedStatus | int
    op: int
    subject: str = ""
    files: list[File] = Field(default_factory=list)
    email: str = ""
    name: str = ""
    trip: str = ""
    icon: str | None = None
    trip_style: str | None = None
    tags: str | None = None
    likes: int | None = None
    dislikes: int | None = None
    number: int | None = None
    unique_posters: int | str | None = None
    files_count: int | None = None
    posts_count: int | None = None

    @field_validator("files", mode="before")
    @classmethod
    def empty_files(cls, value: object) -> object:
        return [] if value is None else value

    @property
    def header(self) -> str:
        return clear_html(self.subject)

    @property
    def body(self) -> str:
        return convert_html(self.comment)

    @property
    def body_text(self) -> str:
        return clear_html(self.comment)

    @property
    def post_id(self) -> int:
        return self.num

    @property
    def parent_id(self) -> int:
        return self.parent or self.num

    def dt(self, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp, tz=tz)

    def dt_last_post(self, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.lasthit, tz=tz)

    def url(self, base_url: str = API_BASE) -> str:
        return f"{base_url.rstrip('/')}/{self.board}/res/{self.parent_id}.html#{self.post_id}"
