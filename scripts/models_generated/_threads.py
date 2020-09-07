# generated by datamodel-codegen:
#   filename:  threads
#   timestamp: 2020-09-07T14:20:16+00:00

from typing import List

from pydantic import BaseModel


class Thread(BaseModel):
    comment: str
    lasthit: int
    num: str
    posts_count: int
    score: float
    subject: str
    timestamp: int
    views: int


class Model(BaseModel):
    board: str
    threads: List[Thread]
