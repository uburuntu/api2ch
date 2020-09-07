import pytest

from api2ch import Api2chAsync, Api2chError


@pytest.mark.asyncio
class TestApiAsync:
    async def test_thread(self, api_async: Api2chAsync):
        await api_async.thread('api', 1)

        with pytest.raises(Api2chError):
            await api_async.thread('b', 1)

    async def test_threads(self, api_async: Api2chAsync):
        (await api_async.threads('b')).sorted_by_views()
        (await api_async.threads('hw')).sorted_by_posts_count()
        (await api_async.threads('test')).sorted_by_score()

    async def test_catalog(self, api_async: Api2chAsync):
        await api_async.catalog('au')
        await api_async.catalog('fiz')
        await api_async.catalog('sci')

    async def test_catalog_by_date(self, api_async: Api2chAsync):
        await api_async.catalog_by_date('au')
        await api_async.catalog_by_date('fiz')
        await api_async.catalog_by_date('sci')

    async def test_page(self, api_async: Api2chAsync):
        await api_async.page('au', 'index')
        await api_async.page('fiz', 'index')
        await api_async.page('sci', 'index')

    async def test_boards(self, api_async: Api2chAsync):
        await api_async.boards()

    async def test_boards_by_types(self, api_async: Api2chAsync):
        await api_async.boards_by_types()

    async def test_thread_posts_by_num(self, api_async: Api2chAsync):
        await api_async.thread_posts_by_num('api', 1, 1)

    async def test_thread_posts_by_post(self, api_async: Api2chAsync):
        await api_async.thread_posts_by_post('api', 1, 1)

    async def test_single_post(self, api_async: Api2chAsync):
        await api_async.single_post('api', 1)
