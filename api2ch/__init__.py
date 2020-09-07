"""Async API Wrapper for 2ch Imageboard with typings"""

from .api import Api2ch, Api2chAsync, Api2chBase, Api2chError
from .models.auxiliary import NewsAbuItem, Tag, TopItem
from .models.base import Base, Request, Response
from .models.board import Board, BoardInfo, BoardInfoBase, BoardInfoMini
from .models.file import File
from .models.post import Post
from .models.request import RequestBoards, RequestBoardsByTypes, RequestCatalog, RequestCatalogByDate, RequestPage, RequestSinglePost, \
    RequestThread, RequestThreadPostsByNum, RequestThreadPostsByPost, RequestThreads
from .models.response import ResponseBoards, ResponseBoardsByTypes, ResponseCatalog, ResponseCatalogByDate, ResponsePage, \
    ResponseSinglePost, ResponseThread, ResponseThreadPostsByNum, ResponseThreadPostsByPost, ResponseThreads
from .models.thread import Thread, ThreadWithStats

__author__ = 'uburuntu'
__email__ = 'github@rmbk.me'

__license__ = 'MIT'
__version__ = '0.1.0'
