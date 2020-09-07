from typing import Union

from api2ch.models.base import Request
from api2ch.models.response import ResponseBoards, ResponseBoardsByTypes, ResponseCatalog, ResponseCatalogByDate, ResponsePage, \
    ResponseSinglePost, ResponseThread, ResponseThreadPostsByNum, ResponseThreadPostsByPost, ResponseThreads


class RequestThread(Request):
    __returning__ = ResponseThread

    board: str
    thread: Union[str, int]

    def url(self, base: str) -> str:
        return f'{base}/{self.board}/res/{self.thread}.json'


class RequestThreads(Request):
    __returning__ = ResponseThreads

    board: str

    def url(self, base: str) -> str:
        return f'{base}/{self.board}/threads.json'


class RequestCatalog(Request):
    __returning__ = ResponseCatalog

    board: str

    def url(self, base: str) -> str:
        return f'{base}/{self.board}/catalog.json'


class RequestCatalogByDate(Request):
    __returning__ = ResponseCatalogByDate

    board: str

    def url(self, base: str) -> str:
        return f'{base}/{self.board}/catalog_num.json'


class RequestPage(Request):
    __returning__ = ResponsePage

    board: str
    page: Union[str, int]

    def url(self, base: str) -> str:
        return f'{base}/{self.board}/{self.page}.json'


class RequestBoards(Request):
    __returning__ = ResponseBoards

    def url(self, base: str) -> str:
        return f'{base}/boards.json'


class RequestBoardsByTypes(Request):
    __returning__ = ResponseBoardsByTypes

    def url(self, base: str) -> str:
        return f'{base}/makaba/mobile.fcgi?task=get_boards'


class RequestThreadPostsByNum(Request):
    __returning__ = ResponseThreadPostsByNum

    board: str
    thread: Union[str, int]
    num: Union[str, int]

    def url(self, base: str) -> str:
        return f'{base}/makaba/mobile.fcgi?task=get_thread&board={self.board}&thread={self.thread}&num={self.num}'


class RequestThreadPostsByPost(Request):
    __returning__ = ResponseThreadPostsByPost

    board: str
    thread: Union[str, int]
    post: Union[str, int]

    def url(self, base: str) -> str:
        return f'{base}/makaba/mobile.fcgi?task=get_thread&board={self.board}&thread={self.thread}&post={self.post}'


class RequestSinglePost(Request):
    __returning__ = ResponseSinglePost

    board: str
    post: Union[str, int]

    def url(self, base: str) -> str:
        return f'{base}/makaba/mobile.fcgi?task=get_post&board={self.board}&post={self.post}'
