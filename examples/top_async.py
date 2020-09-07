import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        boards = await api.boards_by_types()

        coros = [api.threads(board.id) for board in boards.Technology]

        for coro in asyncio.as_completed(coros):
            threads = await coro
            top_thread = threads.sorted_by_views()[0]
            print(f'— /{threads.request.board} | Top thread: {top_thread.subject}, {top_thread.views} 👁‍🗨')


asyncio.run(main())
