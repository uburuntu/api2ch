from pydantic import Field

from api2ch.models.auxiliary import ThreadInfo, UpstreamError
from api2ch.models.base import Base
from api2ch.models.board import Board
from api2ch.models.post import Post
from api2ch.models.thread import Thread, ThreadSummary


class ResponseThread(Base):
    board: Board
    current_thread: int
    files_count: int
    is_board: bool
    is_closed: int
    is_index: bool
    max_num: int
    posts_count: int
    thread_first_image: str
    threads: list[Thread]
    title: str
    unique_posters: int | str
    advert_mobile_image: str | None = None
    advert_mobile_link: str | None = None
    board_banner_image: str | None = None
    board_banner_link: str | None = None

    @property
    def posts(self) -> list[Post]:
        return self.threads[0].posts if self.threads else []


class ResponseThreads(Base):
    board: str
    threads: list[ThreadSummary]

    def sorted_by_views(self, reverse: bool = True) -> list[ThreadSummary]:
        return sorted(self.threads, key=lambda thread: thread.views, reverse=reverse)

    def sorted_by_posts_count(self, reverse: bool = True) -> list[ThreadSummary]:
        return sorted(self.threads, key=lambda thread: thread.posts_count, reverse=reverse)

    def sorted_by_score(self, reverse: bool = True) -> list[ThreadSummary]:
        return sorted(self.threads, key=lambda thread: thread.score, reverse=reverse)

    def sorted_by_creation(self, reverse: bool = True) -> list[ThreadSummary]:
        return sorted(self.threads, key=lambda thread: thread.timestamp, reverse=reverse)


class ResponseCatalog(Base):
    board: Board
    filter: str
    threads: list[Post]
    advert_mobile_image: str | None = None
    advert_mobile_link: str | None = None
    board_banner_image: str | None = None
    board_banner_link: str | None = None


ResponseCatalogByDate = ResponseCatalog


class ResponsePage(Base):
    board: Board
    board_speed: int
    current_page: int
    current_thread: int
    is_board: bool
    is_index: bool
    pages: list[int]
    threads: list[Thread]
    advert_mobile_image: str | None = None
    advert_mobile_link: str | None = None
    board_banner_image: str | None = None
    board_banner_link: str | None = None


class ResponseThreadInfo(Base):
    result: int
    thread: ThreadInfo | None = None
    error: UpstreamError | None = None


class ResponseThreadPostsByNum(Base):
    result: int
    unique_posters: int | None = None
    posts: list[Post] = Field(default_factory=list)
    error: UpstreamError | None = None


class ResponseSinglePost(Base):
    result: int
    post: Post | None = None
    error: UpstreamError | None = None


ResponseBoards = list[Board]
ResponseBoardsByTypes = dict[str, list[Board]]
ResponseThreadPostsByPost = ResponseThreadPostsByNum
