import random
from string import ascii_lowercase, digits
from typing import NoReturn

from redis.asyncio.client import Redis


class AuthRepository:
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def get_user_id_by_session_id(self, session_id: str) -> int | None:
        user_id = await self._redis_client.get(f'user_session:{session_id}')
        if user_id is None:
            return None
        return int(user_id)

    async def create_session(self, user_id: int) -> str:
        """Creates session, saves in db and returns access_token."""
        access_token = ''.join(random.choices(ascii_lowercase + digits, k=32))
        await self._redis_client.set(
            f'user_session:{access_token}',
            user_id,
            ex=3600 * 24 * 30  # 30 days lifetime
        )
        return access_token

    async def delete_session(self, session_id: str) -> NoReturn:
        await self._redis_client.delete(f'user_session:{session_id}')
