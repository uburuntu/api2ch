import httpx
import pytest

from api2ch import (
    Api2ch,
    Api2chHTTPError,
    Api2chResponseError,
    Api2chUpstreamError,
)


def test_current_endpoints(api: Api2ch) -> None:
    assert api.boards()[0].id == "pr"
    assert list(api.boards_by_types()) == ["Technology"]
    assert api.threads("pr").sorted_by_views()[0].num == 100
    catalog = api.catalog("pr")
    assert catalog.board.id == "pr"
    assert catalog.threads[0].files[0].type == 999
    assert api.catalog_by_date("pr").filter == "num"
    assert api.page("pr").threads[0].posts[0].files == []
    assert api.thread("pr", 100).posts[0].body_text == "Fixture\nbody"
    assert api.thread_info("pr", 100).posts == 1
    assert api.posts_after("pr", 100, 100).posts[0].num == 100
    assert api.post("pr", 100).num == 100


def test_raw_namespace_bypasses_models(api: Api2ch) -> None:
    result = api.raw.boards()
    assert isinstance(result, list)
    assert result[0]["future_setting"] is True
    assert api.raw.thread_info("pr", 100)["result"] == 1


def test_errors_are_distinct(api: Api2ch) -> None:
    with pytest.raises(Api2chUpstreamError) as upstream:
        api.raw.get("/missing")
    assert upstream.value.code == -3

    with pytest.raises(Api2chHTTPError) as http:
        api.raw.get("/http-error")
    assert http.value.code == 503

    with pytest.raises(Api2chResponseError):
        api.raw.get("/malformed")


def test_input_validation_happens_before_transport(api: Api2ch) -> None:
    with pytest.raises(ValueError):
        api.thread("../pr", 100)
    with pytest.raises(ValueError):
        api.thread("pr", 0)


def test_external_client_is_not_closed(handler) -> None:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    api = Api2ch(client=client)
    api.close()
    assert not client.is_closed
    client.close()


def test_closing_unused_owned_client_does_not_create_one() -> None:
    api = Api2ch()
    api.close()
    assert api._client is None
