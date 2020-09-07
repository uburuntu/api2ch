import asyncio

from api2ch import Api2chAsync


async def main():
    async with Api2chAsync() as api:
        resp = await api.threads('hw')
        for t in resp.threads[:3]:
            print(f'— {t.subject}, {t.posts_count} 💬, {t.views} 👁‍🗨')


asyncio.run(main())
