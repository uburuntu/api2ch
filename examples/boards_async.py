import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        coros = [api.catalog(board) for board in ('spc', 'un', 'math')]

        for coro in asyncio.as_completed(coros):
            c = await coro
            print(f'/{c.board} | {c.board_name}, "{c.board_info_outer}", bump limit: {c.bump_limit}')


asyncio.run(main())
