import random
from string import ascii_lowercase, digits

from aioredis import Redis


class CRUDUserSessions:
    @staticmethod
    async def get_user_id_by_session_id(session_id: str, redis_cursor: Redis) -> int | None:
        """Returns user id by session_id cookie value."""
        return await redis_cursor.get(f'user_session:{session_id}')

    @staticmethod
    async def create(user_id: int, redis_cursor: Redis) -> str:
        """Creates session in redis and returns session_id."""
        session_id = ''.join(random.choices(ascii_lowercase + digits, k=32))
        await redis_cursor.set(f'user_session:{session_id}', user_id, ex=3600 * 24 * 30)  # 30 days lifetime
        return session_id

    @staticmethod
    async def delete(session_id: str, redis_cursor: Redis) -> None:
        """Deletes session in redis."""
        await redis_cursor.delete(f'user_session:{session_id}')
