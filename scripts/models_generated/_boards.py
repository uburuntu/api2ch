# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2022-04-30T21:52:43+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Board(BaseModel):
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


class Tag(BaseModel):
    board: str
    tag: str


class Model(BaseModel):
    boards: List[Board]
    global_boards: int
    global_posts: str
    global_speed: str
    is_index: int
    tags: List[Tag]
    type: int
