import pytest

from api2ch import Api2ch, Api2chAsync, Api2chError

pytestmark = pytest.mark.integration


def _active_thread(api: Api2ch) -> tuple[str, int]:
    available = {board.id for board in api.boards()}
    for board in ("pr", "hw", "sci", "test"):
        if board not in available:
            continue
        try:
            threads = api.threads(board).threads
        except Api2chError:
            continue
        if threads:
            return board, threads[0].num
    raise AssertionError("no active non-adult integration board was available")


def test_live_sync_contract() -> None:
    with Api2ch() as api:
        board, thread_id = _active_thread(api)
        assert api.catalog(board).board.id == board
        assert api.catalog_by_date(board).board.id == board
        assert api.page(board).board.id == board
        thread = api.thread(board, thread_id)
        assert thread.posts[0].num == thread_id
        assert api.thread_info(board, thread_id).num == thread_id
        assert api.posts_after(board, thread_id, thread_id).posts[0].num == thread_id
        assert api.post(board, thread_id).num == thread_id


@pytest.mark.asyncio
async def test_live_async_contract() -> None:
    async with Api2chAsync() as api:
        boards = {board.id for board in await api.boards()}
        board = next(candidate for candidate in ("pr", "hw", "sci", "test") if candidate in boards)
        summaries = await api.threads(board)
        assert summaries.threads
        thread_id = summaries.threads[0].num
        assert (await api.catalog(board)).board.id == board
        assert (await api.catalog_by_date(board)).board.id == board
        assert (await api.page(board)).board.id == board
        thread = await api.thread(board, thread_id)
        assert thread.posts[0].num == thread_id
        assert (await api.thread_info(board, thread_id)).num == thread_id
        assert (await api.posts_after(board, thread_id, thread_id)).posts[0].num == thread_id
        assert (await api.post(board, thread_id)).num == thread_id
