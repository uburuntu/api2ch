import datetime

from pydantic import Field

from api2ch.config import API_BASE
from api2ch.models.base import Base
from api2ch.models.post import Post
from api2ch.utils import clear_html, convert_html


class Thread(Base):
    posts: list[Post] = Field(default_factory=list)
    thread_num: int | None = None
    files_count: int | None = None
    posts_count: int | None = None


class ThreadSummary(Base):
    num: int
    timestamp: int
    lasthit: int
    views: int
    posts_count: int
    score: float
    subject: str = ""
    comment: str = ""

    @property
    def thread_id(self) -> int:
        return self.num

    @property
    def header(self) -> str:
        return clear_html(self.subject)

    @property
    def body(self) -> str:
        return convert_html(self.comment)

    @property
    def body_text(self) -> str:
        return clear_html(self.comment)

    def dt(self, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp, tz=tz)

    def dt_last_post(self, tz: datetime.tzinfo | None = None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.lasthit, tz=tz)

    def url(self, board: str, base_url: str = API_BASE) -> str:
        return f"{base_url.rstrip('/')}/{board}/res/{self.thread_id}.html"


ThreadWithStats = ThreadSummary
