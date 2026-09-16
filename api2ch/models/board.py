from pydantic import Field

from api2ch.models.auxiliary import Icon
from api2ch.models.base import Base


class Board(Base):
    id: str
    name: str
    category: str
    info: str = ""
    info_outer: str = ""
    threads_per_page: int
    bump_limit: int
    max_pages: int
    default_name: str
    enable_names: bool
    enable_trips: bool
    enable_subject: bool
    enable_sage: bool
    enable_icons: bool
    enable_flags: bool
    enable_dices: bool
    enable_shield: bool
    enable_thread_tags: bool
    enable_posting: bool
    enable_likes: bool
    enable_oekaki: bool
    file_types: list[str] = Field(default_factory=list)
    max_comment: int
    max_files_size: int
    tags: list[str] = Field(default_factory=list)
    icons: list[Icon] = Field(default_factory=list)


# Compatibility names for code that imported the 1.x model hierarchy.
BoardInfoBase = Board
BoardInfoMini = Board
BoardInfo = Board
