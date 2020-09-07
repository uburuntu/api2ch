import pytest

from api2ch import Api2ch, Api2chError


class TestApi:
    def test_thread(self, api: Api2ch):
        api.thread('api', 1)

        with pytest.raises(Api2chError):
            api.thread('b', 1)

    def test_threads(self, api: Api2ch):
        api.threads('b').sorted_by_views()
        api.threads('hw').sorted_by_posts_count()
        api.threads('test').sorted_by_score()

    def test_catalog(self, api: Api2ch):
        api.catalog('au')
        api.catalog('fiz')
        api.catalog('sci')

    def test_catalog_by_date(self, api: Api2ch):
        api.catalog_by_date('au')
        api.catalog_by_date('fiz')
        api.catalog_by_date('sci')

    def test_page(self, api: Api2ch):
        api.page('au', 'index')
        api.page('fiz', 'index')
        api.page('sci', 'index')

    def test_boards(self, api: Api2ch):
        api.boards()

    def test_boards_by_types(self, api: Api2ch):
        api.boards_by_types()

    def test_thread_posts_by_num(self, api: Api2ch):
        api.thread_posts_by_num('api', 1, 1)

    def test_thread_posts_by_post(self, api: Api2ch):
        api.thread_posts_by_post('api', 1, 1)

    def test_single_post(self, api: Api2ch):
        api.single_post('api', 1)
