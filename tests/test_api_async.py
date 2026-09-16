import pytest

from api2ch import Api2chAsync, Api2chUpstreamError


@pytest.mark.asyncio
async def test_current_endpoints(api_async: Api2chAsync) -> None:
    assert (await api_async.boards())[0].id == "pr"
    assert (await api_async.threads("pr")).threads[0].num == 100
    assert (await api_async.catalog("pr")).board.id == "pr"
    assert (await api_async.catalog_by_date("pr")).filter == "num"
    assert (await api_async.page("pr")).threads[0].posts[0].files == []
    assert (await api_async.thread("pr", 100)).posts[0].num == 100
    assert (await api_async.thread_info("pr", 100)).num == 100
    assert (await api_async.posts_after("pr", 100, 100)).posts[0].num == 100
    assert (await api_async.post("pr", 100)).num == 100


@pytest.mark.asyncio
async def test_raw_and_upstream_error(api_async: Api2chAsync) -> None:
    assert (await api_async.raw.boards())[0]["future_setting"] is True
    with pytest.raises(Api2chUpstreamError) as error:
        await api_async.raw.get("/missing")
    assert error.value.code == -3
