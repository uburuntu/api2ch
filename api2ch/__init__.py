"""Async API Wrapper for 2ch Imageboard with typings"""

from .api import Api2ch, Api2chAsync, Api2chBase, Api2chError
from .config import API_BASE, BOARDS, api_mirrors, downloads_dir
from .helpers import download_thread_media
from .models.auxiliary import BannedStatus, NewsAbuItem, Tag, TopItem
from .models.base import Base, Request, Response
from .models.board import Board, BoardInfo, BoardInfoBase, BoardInfoMini
from .models.file import File
from .models.post import Post
from .models.request import RequestBoards, RequestBoardsByTypes, RequestCatalog, RequestCatalogByDate, RequestPage, RequestSinglePost, \
    RequestThread, RequestThreadPostsByNum, RequestThreadPostsByPost, RequestThreads
from .models.response import ResponseBoards, ResponseBoardsByTypes, ResponseCatalog, ResponseCatalogByDate, ResponsePage, \
    ResponseSinglePost, ResponseThread, ResponseThreadPostsByNum, ResponseThreadPostsByPost, ResponseThreads
from .models.thread import Thread, ThreadWithStats
from .utils import clear_html, convert_html, parse_url

__author__ = 'uburuntu'
__email__ = 'github@rmbk.me'

__license__ = 'MIT'
__version__ = '1.1.7'
