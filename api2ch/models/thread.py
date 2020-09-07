import datetime
from typing import List, Optional

from api2ch.config import API_BASE
from api2ch.models.base import Base
from api2ch.models.post import Post
from api2ch.utils import clear_html, convert_html


class Thread(Base):
    posts: Optional[List[Post]]


class ThreadWithStats(Thread):
    subject: str

    @property
    def header(self):
        return clear_html(self.subject)

    comment: str

    @property
    def body(self):
        return convert_html(self.comment)

    @property
    def body_text(self):
        return clear_html(self.comment)

    num: int

    @property
    def thread_id(self) -> int:
        return self.num

    def url(self, board: str) -> str:
        return f'{API_BASE}/{board}/res/{self.thread_id}.html'

    timestamp: int

    def dt(self, tz=None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp, tz=tz)

    lasthit: int

    def dt_last_post(self, tz=None) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.lasthit, tz=tz)

    views: int
    posts_count: int
    score: float
