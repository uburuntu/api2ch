from enum import IntEnum

from api2ch.models.base import Base


class BannedStatus(IntEnum):
    nothing = 0
    banned = 1
    warning = 2


class Icon(Base):
    name: str
    num: int
    url: str


class UpstreamError(Base):
    code: int
    message: str


class ThreadInfo(Base):
    num: int
    timestamp: int
    posts: int
