from api2ch.models.base import Base


class NewsAbuItem(Base):
    date: str
    num: int
    subject: str
    views: int


class TopItem(Base):
    board: str
    info: str
    name: str


class Tag(Base):
    board: str
    tag: str
