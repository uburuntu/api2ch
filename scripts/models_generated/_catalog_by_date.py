# generated by datamodel-codegen:
#   filename:  catalog_by_date
#   timestamp: 2020-09-07T14:20:16+00:00

from typing import List, Optional

from pydantic import BaseModel


class NewsAbuItem(BaseModel):
    date: str
    num: int
    subject: str
    views: int


class File(BaseModel):
    displayname: str
    fullname: Optional[str] = None
    height: int
    md5: Optional[str] = None
    name: str
    nsfw: Optional[int] = None
    path: str
    size: int
    thumbnail: str
    tn_height: int
    tn_width: int
    type: int
    width: int
    duration: Optional[str] = None
    duration_secs: Optional[int] = None
    install: Optional[str] = None
    pack: Optional[str] = None
    sticker: Optional[str] = None


class Thread(BaseModel):
    banned: int
    closed: int
    comment: str
    date: str
    email: str
    endless: int
    files: List[File]
    files_count: int
    lasthit: int
    name: str
    num: str
    op: int
    parent: str
    posts_count: int
    sticky: int
    subject: str
    tags: str
    timestamp: int
    trip: str


class TopItem(BaseModel):
    board: str
    info: str
    name: str


class Model(BaseModel):
    Board: str
    BoardInfo: str
    BoardInfoOuter: str
    BoardName: str
    advert_bottom_image: str
    advert_bottom_link: str
    advert_mobile_image: str
    advert_mobile_link: str
    advert_top_image: str
    advert_top_link: str
    board_banner_image: str
    board_banner_link: str
    bump_limit: int
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_images: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    enable_video: int
    filter: str
    max_comment: int
    max_files_size: int
    news_abu: List[NewsAbuItem]
    threads: List[Thread]
    top: List[TopItem]
