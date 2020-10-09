import re
from typing import Tuple
from urllib.parse import ParseResult, urlparse

from api2ch.config import BOARDS, hostname_mirrors


def prettify_bytes(size: float) -> str:
    for unit in ('Б', 'Кб', 'Мб', 'Гб', 'Тб'):
        if size < 1024.0:
            break
        size /= 1024.0
    return f'{size:.0f} {unit}' if unit in ('Б', 'Кб') else f'{size:.2f} {unit}'


def parse_url(url: str) -> Tuple[bool, str, int]:
    """
    Parse url with checks
    :param url: example: 'https://2ch.hk/api/res/1.html'
    :return: is_valid, board, thread_id
    """
    result: ParseResult = urlparse(url)
    bad = False, '', 0

    if result.hostname not in hostname_mirrors:
        return bad

    split = re.split('[/.]', result.path)
    if len(split) < 3:
        return bad

    board, method, thread = split[1], split[2], split[3]
    if board not in BOARDS or method != 'res' or not thread.isdigit():
        return bad

    thread_id = int(thread)
    return True, board, thread_id


def convert_html(text: str) -> str:
    """Telegram acceptable HTML code"""
    text = re.sub(r'<br>', '\n', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&quot;', '\'', text)
    text = re.sub(r'&#47;', '/', text)

    text = re.sub(r'<(/?)strong>', r'<\1b>', text)
    text = re.sub(r'<(/?)em>', r'<\1i>', text)

    text = re.sub(r'</?span.*?>', '', text)
    text = re.sub(r'</?sup>', '', text)
    text = re.sub(r'</?sup>', '', text)
    return text


def clear_html(text: str) -> str:
    """Clear text from HTML tags"""
    text = re.sub(r'<br>', '\n', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&quot;', '\'', text)
    text = re.sub(r'&#47;', '/', text)

    text = re.sub(r'<.*?>', '', text)
    return text
