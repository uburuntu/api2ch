import html
import re
from html.parser import HTMLParser
from urllib.parse import urlparse

from api2ch.config import hostname_mirrors


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def prettify_bytes(size: float) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    index = 0
    while size >= 1024.0 and index < len(units) - 1:
        size /= 1024.0
        index += 1
    unit = units[index]
    return f"{size:.0f} {unit}" if unit in {"B", "KiB"} else f"{size:.2f} {unit}"


def parse_url(url: str) -> tuple[bool, str, int]:
    """Parse a 2ch thread URL without relying on a frozen board list."""

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in hostname_mirrors:
        return False, "", 0

    match = re.fullmatch(r"/([a-z0-9_]+)/res/([1-9][0-9]*)\.html/?", parsed.path)
    if match is None:
        return False, "", 0
    return True, match.group(1), int(match.group(2))


def clear_html(text: str) -> str:
    parser = _TextExtractor()
    parser.feed(text)
    parser.close()
    return "".join(parser.parts)


def convert_html(text: str) -> str:
    """Convert the small upstream markup subset to conservative rich text."""

    converted = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    converted = re.sub(r"<(\/?)strong>", r"<\1b>", converted, flags=re.IGNORECASE)
    converted = re.sub(r"<(\/?)em>", r"<\1i>", converted, flags=re.IGNORECASE)
    converted = re.sub(r"</?(?:span|sup|sub)(?:\s[^>]*)?>", "", converted, flags=re.IGNORECASE)
    return html.unescape(converted)
