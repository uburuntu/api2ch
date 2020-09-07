from typing import List, Optional

from api2ch.models.base import Base
from api2ch.models.file import File


class Post(Base):
    banned: int
    closed: int
    comment: str
    date: str
    email: str
    endless: int
    files: List[File]
    lasthit: int
    name: str
    num: int
    number: Optional[int]
    op: int
    parent: str
    sticky: int
    subject: str
    tags: Optional[str]
    timestamp: int
    trip: str
    trip_type: Optional[str]
    unique_posters: Optional[str]
    files_count: Optional[int]
    posts_count: Optional[int]
