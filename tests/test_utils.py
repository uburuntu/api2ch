from api2ch import clear_html, convert_html, parse_url


def test_parse_url_accepts_current_origin_and_new_board_ids() -> None:
    assert parse_url("https://2ch.su/new_board/res/123.html#456") == (True, "new_board", 123)
    assert parse_url("https://example.com/pr/res/123.html") == (False, "", 0)
    assert parse_url("https://2ch.su/pr") == (False, "", 0)


def test_text_helpers() -> None:
    assert clear_html("one<br><strong>two</strong>") == "one\ntwo"
    assert convert_html("one<br><strong>two</strong>") == "one\n<b>two</b>"
