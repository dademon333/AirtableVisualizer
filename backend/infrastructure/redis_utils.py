from typing import AsyncIterator

from redis.asyncio.client import Redis

from tokens import REDIS_HOST


async def get_redis_client() -> AsyncIterator[Redis]:
    client = Redis.from_url(f'redis://{REDIS_HOST}')
    try:
        yield client
    finally:
        await client.close()
