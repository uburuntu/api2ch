# api2ch

[![Python](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8-blue.svg?longCache=true)]()
[![PyPI](https://img.shields.io/pypi/v/api2ch.svg)](https://pypi.python.org/pypi/api2ch)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![Build Status](https://travis-ci.org/uburuntu/api2ch.svg?branch=master)](https://travis-ci.org/uburuntu/api2ch)

⚡️ Async API Wrapper for 2ch Imageboard with typings

Docs: https://2ch.hk/api/res/1.html

![](https://i.imgur.com/VLbQhEv.jpg)

## 📝 Table of Contents

- [🎒 Installation](#-installation)
- [🛠 Examples](#-examples)
  - [Simple](#simple)
  - [Simple Async](#simple-async)
  - [Boards](#boards)
  - [Boards Async](#boards-async)
  - [Top threads](#top-threads)
  - [Top Threads Async](#top-threads-async)
- [📜 Manual](#-manual)
  - [Methods](#methods)
  - [Types](#types)
  - [In case of unsupported types](#in-case-of-unsupported-types)
- [💬 Contributing](#-contributing)
- [📝 License](#-license)


---

## 🎒 Installation
Just
```
pip install api2ch
```

## 🛠 Examples

### Simple

```python3
from api2ch import Api2ch

api = Api2ch()

resp = api.threads('vg')
for t in resp.threads[:3]:
    print(f'— {t.subject}, {t.posts_count} 💬, {t.views} 👁')
```
Output:
```text
— Paradox Thread №6 стрессовый, 771 💬, 1879 👁
— BioWare General: Varric Tethras Edition, 207 💬, 644 👁
— Fate/Grand Order #193, 683 💬, 4804 👁
```

### Simple Async

```python3
import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        resp = await api.threads('hw')
        for t in resp.threads[:3]:
            print(f'— {t.subject}, {t.posts_count} 💬, {t.views} 👁')


asyncio.run(main())
```
Output:
```text
— Видеокарты AMD #95, 418 💬, 3778 👁
— Сап. Впервые в этом разделе. Как научится разбираться в железе?, 3 💬, 9 👁
— Ноутбукотред №36, 185 💬, 970 👁
```

### Boards

```python3
from api2ch import Api2ch

api = Api2ch()

for board in ('tv', 'hw', 'fiz'):
    c = api.catalog(board)
    print(f'/{c.board} | {c.board_name}, "{c.board_info_outer}", bump limit: {c.bump_limit}')
```
Output:
```text
/tv | Сериалы, "сериалы для домохозяек, игры престолов в /got/", bump limit: 500
/hw | Компьютерное железо, "железо, видеокарты, ноутбуки, intel, amd, nvidia, ati", bump limit: 500
/fiz | Физкультура, "физкультура, здоровье, сбросить вес, набрать вес, бицуха", bump limit: 800
```

### Boards Async

```python3
import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        coros = [api.catalog(board) for board in ('spc', 'un', 'math')]

        for coro in asyncio.as_completed(coros):
            c = await coro
            print(f'/{c.board} | {c.board_name}, "{c.board_info_outer}", bump limit: {c.bump_limit}')


asyncio.run(main())
```
Output:
```text
/un | Образование, "образование, вуз, школа, поступление, гиа, егэ, уже не школьник", bump limit: 500
/spc | Космос и астрономия, "космос, астрономия, вселенные, звезды, огурцы", bump limit: 500
/math | Математика, "Доска о модулях над кольцами, пучках на многообразиях и гомологиях с когомологиями.", bump limit: 500
```

### Top threads

```python3
from api2ch import Api2ch

api = Api2ch()

boards = api.boards_by_types()
for board in boards.Art:
    threads = api.threads(board.id)
    top_thread = threads.sorted_by_views()[0]
    print(f'— /{threads.request.board} | {board.name} | Top thread: {top_thread.subject}, {top_thread.views} 👁')
```
Output:
```text
— /di | Столовая | Top thread: НОВОЙ БАНОЧКИ НИТЬ ИДИ, 123475 👁
— /de | Дизайн | Top thread: Зарплата, 48958 👁
— /diy | Хобби | Top thread: Кристаллический тред, 1620541 👁
— /mus | Музыканты | Top thread: Язычковых тред., 153772 👁
— /pa | Живопись | Top thread: Сталин 3000, 40392 👁
— /p | Фотография | Top thread: Ссылкотред, 34182 👁
— /wp | Обои и высокое разрешение | Top thread: Милитари пак, 38348 👁
— /wrk | Работа и карьера | Top thread: Яндекс Дзена /zen тред 11, 33648 👁
```

### Top Threads Async

```python3
import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        boards = await api.boards_by_types()

        coros = [api.threads(board.id) for board in boards.Technology]

        for coro in asyncio.as_completed(coros):
            threads = await coro
            top_thread = threads.sorted_by_views()[0]
            print(f'— /{threads.request.board} | Top thread: {top_thread.subject}, {top_thread.views} 👁')


asyncio.run(main())
```
Output:
```text
— /ra | Top thread: OsmocomBB - Motorola, 1517590 👁
— /hw | Top thread: VR тред возрожденный #4, 17638 👁
— /t | Top thread: Выбираем робот-пылесос, 22336 👁
— /s | Top thread: Форки лиса, 49613 👁
— /pr | Top thread: Советов ньюфагу тред, 25838 👁
— /gd | Top thread: В этом треде ищем напарников для создания своих, 38633 👁
— /mobi | Top thread: PUBG MOBILE/Пупок мобайл-THREAD, 70643 👁
```

## 📜 Manual

### Methods
`Api2ch` methods (and same for `Api2chAsync` but with `async`):
```python3
class Api2ch(Api2chBase):
    ...
    def thread(self, board: str, thread: Union[str, int]) -> ResponseThread:
        ...
    def threads(self, board: str) -> ResponseThreads:
        ...
    def catalog(self, board: str) -> ResponseCatalog:
        ...
    def catalog_by_date(self, board: str) -> ResponseCatalogByDate:
        ...
    def page(self, board: str, page: Union[str, int]) -> ResponsePage:
        ...
    def boards(self) -> ResponseBoards:
        ...
    def boards_by_types(self) -> ResponseBoardsByTypes:
        ...
    def thread_posts_by_num(self, board: str, thread: Union[str, int], num: Union[str, int]) -> ResponseThreadPostsByNum:
        ...
    def thread_posts_by_post(self, board: str, thread: Union[str, int], post: Union[str, int]) -> ResponseThreadPostsByPost:
        ...
    def single_post(self, board: str, post: Union[str, int]) -> ResponseSinglePost:
        ...
```

### Types
This library uses [pydantic](https://github.com/samuelcolvin/pydantic/) for parsing API responses.
You can see data models in [api2ch/models](api2ch/models).

### In case of unsupported types
API results can change and the library may not parse the new result. So you can request «raw» dicts: 
```python3
api = Api2ch(raw_results=True)
```

## 💬 Contributing

Contributions, issues and feature requests are welcome! 

## 📝 License

This project is [MIT](LICENSE) licensed.
