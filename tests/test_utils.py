from api2ch import clear_html, convert_html, parse_url
from api2ch.utils import prettify_bytes


def test_parse_url():
    assert parse_url('https://2ch.hk/api/res/1.html') == (True, 'api', 1)
    assert parse_url('https://example.com/api/res/1.html') == (False, '', 0)


def test_convert_html():
    assert convert_html('<strong>hello</strong><br><em>world</em>') == '<b>hello</b>\n<i>world</i>'


def test_clear_html():
    assert clear_html('<span>hello</span><br>&quot;world&quot;') == "hello\n'world'"


def test_prettify_bytes():
    assert prettify_bytes(1024) == '1 Кб'
    assert prettify_bytes(1024 * 1024) == '1.00 Мб'
