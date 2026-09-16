import pytest
import pytest_asyncio

from api2ch import Api2ch, Api2chAsync


@pytest.fixture
def api():
    with Api2ch() as api:
        yield api


@pytest_asyncio.fixture
async def api_async():
    async with Api2chAsync() as api:
        yield api
