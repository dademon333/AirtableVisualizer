import asyncio
import traceback

from common import cache


class CacheUpdater:
    @classmethod
    async def init(cls):
        while True:
            try:
                await cache.update_cache()
                await asyncio.sleep(300)
            except:
                traceback.print_exc()
                await asyncio.sleep(300)
