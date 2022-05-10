from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis.client import Redis

import crud
from db import UserStatus, user_status_weights, get_db
from common.project_cookies import ProjectCookies, get_delete_cookie_header
from common.redis import get_redis_cursor


async def get_user_id(
        redis_cursor: Redis = Depends(get_redis_cursor),
        session_id: str = Cookie(default=None, include_in_schema=False)
) -> int | None:
    """Returns user id by 'session_id' cookie.

    If session_id passed, but invalid, returns response with 403 status and drops 'session_id' cookie.
    """
    if session_id is None:
        return None

    user_id = await crud.user_sessions.get_user_id_by_session_id(session_id, redis_cursor)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'set-cookie': get_delete_cookie_header(ProjectCookies.SESSION_ID)}
        )
    return int(user_id)


async def get_user_status(
        db: AsyncSession = Depends(get_db),
        user_id: int | None = Depends(get_user_id)
) -> UserStatus | None:
    if user_id is None:
        return None

    # If user was deleted, but session wasn't
    if (user := await crud.users.get_by_id(db, user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'set-cookie': get_delete_cookie_header(ProjectCookies.SESSION_ID)}
        )
    return user.status


def can_access(
        user_status: UserStatus | None,
        min_status: UserStatus
) -> bool:
    """Returns True, if user status is greater or equal than min_status, else - False."""
    return user_status_weights[user_status] >= user_status_weights[min_status]


async def check_auth(
        user_id: int | None = Depends(get_user_id)
):
    """Ensured that user is authorized.

    If not, returns 401 UNAUTHORIZED.
    Usage example:
    @router.get(
        '/test_endpoint',
        dependencies=[Depends(check_auth)]
    )
    async def test():
        ...
    """
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


class UserStatusChecker:
    def __init__(self, min_status: UserStatus):
        """Ensures that status of user, who calls endpoint, is more or equal to min_status.
        If not, returns 403 Forbidden.

        Usage example:
        @router.get(
            '/test_endpoint',
            dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
        )
        async def test():
            ...
        """
        self.min_status = min_status

    def __call__(self, user_status: UserStatus | None = Depends(get_user_status)):
        if user_status is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if user_status_weights[user_status] < user_status_weights[self.min_status]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'This operation requires minimum {self.min_status.value} status'
            )
