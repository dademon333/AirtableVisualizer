from typing import NoReturn

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio.client import Redis

from auth.exceptions import UnauthorizedError, LowStatusError
from auth.repository import AuthRepository
from auth.use_cases.login import LoginUseCase
from auth.use_cases.logout import LogoutUseCase
from infrastructure.db import UserStatus, user_status_weights
from infrastructure.redis_utils import get_redis_client
from users.di import get_user_repository
from users.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'/login', auto_error=False)


def get_auth_repository(
        redis_client: Redis = Depends(get_redis_client),
) -> AuthRepository:
    return AuthRepository(redis_client)


def get_login_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_repository: AuthRepository = Depends(get_auth_repository),
) -> LoginUseCase:
    return LoginUseCase(auth_repository, user_repository)


def get_logout_use_case(
        auth_repository: AuthRepository = Depends(get_auth_repository),
) -> LogoutUseCase:
    return LogoutUseCase(auth_repository)


async def get_user_id_soft(
        access_token: str | None = Depends(oauth2_scheme),
        auth_repository: AuthRepository = Depends(get_auth_repository),
) -> int | None:
    """Returns user id by 'Authorization' header.

    If access_token passed, but invalid, raises 401 UNAUTHORIZED.
    """
    if access_token is None:
        return None

    user_id = await auth_repository.get_user_id_by_token(access_token)
    if not user_id:
        raise UnauthorizedError()
    return user_id


async def get_user_id(
        user_id: int | None = Depends(get_user_id_soft),
) -> int:
    """Strict version of get_user_id. Raises 401, if user not authenticated."""
    if user_id is None:
        raise UnauthorizedError()
    return user_id


async def get_user_status(
        user_id: int | None = Depends(get_user_id_soft),
        user_repository: UserRepository = Depends(get_user_repository),
) -> UserStatus | None:
    if user_id is None:
        return None

    # If user was deleted, but access_token wasn't

    user = await user_repository.get_by_id(user_id)
    if not user:
        raise UnauthorizedError()
    return user.status


def can_access(
        user_status: UserStatus | None,
        min_status: UserStatus
) -> bool:
    """Returns True, if user status is greater or equal
    than min_status, else - False.

    """
    return user_status_weights[user_status] >= user_status_weights[min_status]


# noinspection PyUnusedLocal
async def check_auth(
        user_id: int = Depends(get_user_id)
) -> None:
    """Ensures that user is authenticated.

    If not, raises 401 UNAUTHORIZED.
    Usage example:
    @router.get(
        '/test_endpoint',
        dependencies=[Depends(check_auth)]
    )
    async def test():
        ...

    """
    pass


class UserStatusChecker:
    """Ensures that status of user, who calls endpoint, is >= to min_status.
    If not, returns 403 Forbidden.

    Usage example:
    @router.get(
        '/test_endpoint',
        dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
    )
    async def test():
        ...

    """

    def __init__(self, min_status: UserStatus):
        self.min_status = min_status

    def __call__(
            self,
            user_status: UserStatus | None = Depends(get_user_status)
    ) -> NoReturn:
        if user_status is None:
            raise UnauthorizedError()

        user_weight = user_status_weights[user_status]
        min_weight = user_status_weights[self.min_status]
        if user_weight < min_weight:
            raise LowStatusError(min_status=self.min_status)
