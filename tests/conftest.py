import pytest

from api2ch import Api2ch, Api2chAsync


@pytest.fixture
def api():
    with Api2ch() as api:
        yield api


@pytest.fixture
async def api_async():
    async with Api2chAsync() as api:
        yield api
