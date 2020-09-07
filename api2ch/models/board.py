from typing import List

from pydantic import Field

from api2ch.models.auxiliary import NewsAbuItem, TopItem
from api2ch.models.base import Base


class BoardInfoBase(Base):
    bump_limit: int
    default_name: str
    enable_dices: bool
    enable_flags: bool
    enable_icons: bool
    enable_likes: bool
    enable_names: bool
    enable_oekaki: bool
    enable_posting: bool
    enable_sage: bool
    enable_shield: bool
    enable_subject: bool
    enable_thread_tags: bool
    enable_trips: bool


class BoardInfoMini(BoardInfoBase):
    category: str
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class BoardInfo(BoardInfoBase):
    board: str = Field(alias='Board')
    board_info: str = Field(alias='BoardInfo')
    board_info_outer: str = Field(alias='BoardInfoOuter')
    board_name: str = Field(alias='BoardName')
    advert_bottom_image: str
    advert_bottom_link: str
    advert_mobile_image: str
    advert_mobile_link: str
    advert_top_image: str
    advert_top_link: str
    board_banner_image: str
    board_banner_link: str
    enable_images: bool
    enable_video: bool
    max_comment: int
    max_files_size: int
    news_abu: List[NewsAbuItem]
    top: List[TopItem]


class Board(Base):
    bump_limit: int
    category: str
    default_name: str
    enable_names: int
    enable_sage: int
    id: str
    info: str
    last_num: int
    name: str
    speed: int
    threads: int
    unique_posters: int
