from typing import List, Optional

from pydantic import BaseModel, Field, validator

from api2ch.models.auxiliary import Tag
from api2ch.models.base import Response
from api2ch.models.board import Board, BoardInfo, BoardInfoMini
from api2ch.models.post import Post
from api2ch.models.thread import Thread, ThreadWithStats


class ResponseThread(Response, BoardInfo):
    current_thread: str
    files_count: int
    is_board: int
    is_closed: int
    is_index: int
    max_num: int
    posts_count: int
    thread_first_image: str
    threads: List[Thread]
    title: str
    unique_posters: str


class ResponseThreads(Response):
    board: str
    threads: List[ThreadWithStats]

    def sorted_by_views(self, reverse: bool = True) -> List[ThreadWithStats]:
        return sorted(self.threads, key=lambda t: t.views, reverse=reverse)

    def sorted_by_posts_count(self, reverse: bool = True) -> List[ThreadWithStats]:
        return sorted(self.threads, key=lambda t: t.posts_count, reverse=reverse)

    def sorted_by_score(self, reverse: bool = True) -> List[ThreadWithStats]:
        return sorted(self.threads, key=lambda t: t.score, reverse=reverse)


class ResponseCatalog(Response, BoardInfo):
    filter: str
    threads: List[Thread]


class ResponseCatalogByDate(Response, BoardInfo):
    filter: str
    threads: List[Thread]


class ResponsePage(Response, BoardInfo):
    board_speed: int
    current_page: int
    current_thread: int
    is_board: bool
    is_index: bool
    pages: List[int]
    threads: List[Thread]


class ResponseBoards(Response):
    boards: List[Board]
    global_boards: int
    global_posts: str
    global_speed: str
    is_index: int
    tags: List[Tag]
    type: int


class ResponseBoardsByTypes(Response):
    Adult: List[BoardInfoMini] = Field(alias='Взрослым')
    VideoGames: List[BoardInfoMini] = Field(alias='Игры')
    Politics: List[BoardInfoMini] = Field(alias='Политика')
    UserBoards: List[BoardInfoMini] = Field(alias='Пользовательские')
    Misc: List[BoardInfoMini] = Field(alias='Разное')
    Art: List[BoardInfoMini] = Field(alias='Творчество')
    Interests: List[BoardInfoMini] = Field(alias='Тематика')
    Technology: List[BoardInfoMini] = Field(alias='Техника и софт')
    JapaneseCulture: List[BoardInfoMini] = Field(alias='Японская культура')


class ResponseThreadPostsHelper(BaseModel):
    __root__: List[Post]


class ResponseThreadPostsByNum(Response):
    posts: List[Post]

    @classmethod
    def parse_obj(cls, *args, **kwargs):
        h = ResponseThreadPostsHelper.parse_obj(*args, **kwargs)
        return cls(posts=h.__root__)


class ResponseThreadPostsByPost(Response):
    posts: List[Post]

    @classmethod
    def parse_obj(cls, *args, **kwargs):
        h = ResponseThreadPostsHelper.parse_obj(*args, **kwargs)
        return cls(posts=h.__root__)


class ResponseSinglePost(Response):
    post: Optional[Post]

    @classmethod
    def parse_obj(cls, *args, **kwargs):
        h = ResponseThreadPostsHelper.parse_obj(*args, **kwargs)
        return cls(posts=h.__root__)

    @validator('post', pre=True)
    def parse(cls, v):
        if isinstance(v, list):
            if v:
                return v[0]
        return None
