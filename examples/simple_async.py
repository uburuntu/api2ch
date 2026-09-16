import asyncio

from api2ch import Api2chAsync


async def main() -> None:
    async with Api2chAsync() as api:
        threads = await api.threads("hw")
        for thread in threads.sorted_by_views()[:3]:
            print(thread.num, thread.header, thread.views)


asyncio.run(main())
