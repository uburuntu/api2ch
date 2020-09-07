import json
from typing import Union

import aiohttp
import requests

from api2ch.models.request import Request, RequestBoards, RequestBoardsByTypes, RequestCatalog, RequestCatalogByDate, RequestPage, \
    RequestSinglePost, RequestThread, RequestThreadPostsByNum, RequestThreadPostsByPost, RequestThreads
from api2ch.models.response import ResponseBoards, ResponseBoardsByTypes, ResponseCatalog, ResponseCatalogByDate, ResponsePage, \
    ResponseSinglePost, ResponseThread, ResponseThreadPostsByNum, ResponseThreadPostsByPost, ResponseThreads


class Api2chError(Exception):
    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason

    def __repr__(self):
        return f'[{self.code}] {self.reason}'


class Api2chBase:
    """
    Docs: https://2ch.hk/api/res/1.html
    """
    api_base = 'https://2ch.hk'

    def __init__(self, raw_results: bool = False):
        self.raw = raw_results


class Api2ch(Api2chBase):
    @property
    def session(self) -> requests.Session:
        session = getattr(self, '_session', None)
        if session is None:
            session = requests.Session()
            setattr(self, '_session', session)
        return session

    def close(self):
        """
        Closes session
        :return: None
        """
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def request(self, request: Request):
        response = self.session.get(request.url(self.api_base))
        if response.status_code != 200:
            raise Api2chError(response.status_code, response.reason)
        result = json.loads(response.content)
        if self.raw:
            return result
        result = request.__returning__.parse_obj(result)
        result.request = request
        return result

    def thread(self, board: str, thread: Union[str, int]) -> ResponseThread:
        return RequestThread(api=self, board=board, thread=thread).do()

    def threads(self, board: str) -> ResponseThreads:
        return RequestThreads(api=self, board=board).do()

    def catalog(self, board: str) -> ResponseCatalog:
        return RequestCatalog(api=self, board=board).do()

    def catalog_by_date(self, board: str) -> ResponseCatalogByDate:
        return RequestCatalogByDate(api=self, board=board).do()

    def page(self, board: str, page: Union[str, int]) -> ResponsePage:
        return RequestPage(api=self, board=board, page=page).do()

    def boards(self) -> ResponseBoards:
        return RequestBoards(api=self).do()

    def boards_by_types(self) -> ResponseBoardsByTypes:
        return RequestBoardsByTypes(api=self).do()

    def thread_posts_by_num(self, board: str, thread: Union[str, int], num: Union[str, int]) -> ResponseThreadPostsByNum:
        return RequestThreadPostsByNum(api=self, board=board, thread=thread, num=num).do()

    def thread_posts_by_post(self, board: str, thread: Union[str, int], post: Union[str, int]) -> ResponseThreadPostsByPost:
        return RequestThreadPostsByPost(api=self, board=board, thread=thread, post=post).do()

    def single_post(self, board: str, post: Union[str, int]) -> ResponseSinglePost:
        return RequestSinglePost(api=self, board=board, post=post).do()


class Api2chAsync(Api2chBase):
    @property
    def session(self) -> aiohttp.ClientSession:
        session = getattr(self, '_session', None)
        if session is None:
            session = aiohttp.ClientSession()
            setattr(self, '_session', session)
        return session

    async def close(self):
        """
        Closes session
        :return: None
        """
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def request(self, request: Request):
        async with self.session.get(request.url(self.api_base)) as response:
            if response.status != 200:
                raise Api2chError(response.status, response.reason)
            result = json.loads(await response.read())
            if self.raw:
                return result
            result = request.__returning__.parse_obj(result)
            result.request = request
            return result

    async def thread(self, board: str, thread: Union[str, int]) -> ResponseThread:
        return await RequestThread(api=self, board=board, thread=thread).do_async()

    async def threads(self, board: str) -> ResponseThreads:
        return await RequestThreads(api=self, board=board).do_async()

    async def catalog(self, board: str) -> ResponseCatalog:
        return await RequestCatalog(api=self, board=board).do_async()

    async def catalog_by_date(self, board: str) -> ResponseCatalogByDate:
        return await RequestCatalogByDate(api=self, board=board).do_async()

    async def page(self, board: str, page: Union[str, int]) -> ResponsePage:
        return await RequestPage(api=self, board=board, page=page).do_async()

    async def boards(self) -> ResponseBoards:
        return await RequestBoards(api=self).do_async()

    async def boards_by_types(self) -> ResponseBoardsByTypes:
        return await RequestBoardsByTypes(api=self).do_async()

    async def thread_posts_by_num(self, board: str, thread: Union[str, int], num: Union[str, int]) -> ResponseThreadPostsByNum:
        return await RequestThreadPostsByNum(api=self, board=board, thread=thread, num=num).do_async()

    async def thread_posts_by_post(self, board: str, thread: Union[str, int], post: Union[str, int]) -> ResponseThreadPostsByPost:
        return await RequestThreadPostsByPost(api=self, board=board, thread=thread, post=post).do_async()

    async def single_post(self, board: str, post: Union[str, int]) -> ResponseSinglePost:
        return await RequestSinglePost(api=self, board=board, post=post).do_async()
