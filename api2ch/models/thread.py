from typing import List, Optional

from api2ch.models.base import Base
from api2ch.models.post import Post


class Thread(Base):
    posts: Optional[List[Post]]


class ThreadWithStats(Thread):
    comment: str
    lasthit: int
    num: str
    posts_count: int
    score: float
    subject: str
    timestamp: int
    views: int
