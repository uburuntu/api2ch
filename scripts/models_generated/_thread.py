# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2022-04-30T21:52:38+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class NewsAbuItem(BaseModel):
    date: str
    num: int
    subject: str
    views: int


class File(BaseModel):
    displayname: str
    fullname: str
    height: int
    md5: str
    name: str
    nsfw: int
    path: str
    size: int
    thumbnail: str
    tn_height: int
    tn_width: int
    type: int
    width: int


class Post(BaseModel):
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
    number: int
    op: int
    parent: str
    sticky: int
    subject: str
    tags: str
    timestamp: int
    trip: str


class Thread(BaseModel):
    posts: List[Post]


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
    current_thread: str
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
    files_count: int
    is_board: int
    is_closed: int
    is_index: int
    max_comment: int
    max_files_size: int
    max_num: int
    news_abu: List[NewsAbuItem]
    posts_count: int
    thread_first_image: str
    threads: List[Thread]
    title: str
    top: List[TopItem]
    unique_posters: str
