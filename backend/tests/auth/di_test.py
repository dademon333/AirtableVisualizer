from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from auth.di import get_user_id_soft, get_user_id, get_user_status, \
    can_access, UserStatusChecker
from auth.exceptions import UnauthorizedError, LowStatusError
from auth.repository import AuthRepository
from infrastructure.db import User, UserStatus
from users.repository import UserRepository


async def test_get_user_id_soft_no_access_token():
    result = await get_user_id_soft(
        session_id=None,
        auth_repository=Mock(spec=AuthRepository)
    )
    assert result is None


async def test_get_user_id_soft_session_expired():
    repository_mock = Mock(spec=AuthRepository)
    repository_mock.get_user_id_by_session_id = CoroutineMock(return_value=None)

    with pytest.raises(UnauthorizedError):
        await get_user_id_soft(
            session_id="abc",
            auth_repository=repository_mock
        )


async def test_get_user_id_soft_success():
    repository_mock = Mock(spec=AuthRepository)
    repository_mock.get_user_id_by_session_id = CoroutineMock(return_value=123)

    result = await get_user_id_soft(
        session_id="abc",
        auth_repository=repository_mock
    )
    assert result == 123


async def test_get_user_id_no_session():
    with pytest.raises(UnauthorizedError):
        await get_user_id(user_id=None)


async def test_get_user_id_success():
    result = await get_user_id(user_id=123)
    assert result == 123


async def test_get_user_status_no_auth():
    result = await get_user_status(user_id=None, user_repository=Mock())
    assert result is None


async def test_get_user_status_expired_session():
    repository_mock = Mock(spec=UserRepository)
    repository_mock.get_by_id = CoroutineMock(return_value=None)

    with pytest.raises(UnauthorizedError):
        await get_user_status(user_id=1, user_repository=repository_mock)


async def test_get_user_status_success(user: User):
    repository_mock = Mock(spec=UserRepository)
    repository_mock.get_by_id = CoroutineMock(return_value=user)

    result = await get_user_status(user_id=1, user_repository=repository_mock)
    assert result == user.status


@pytest.mark.parametrize(
    "user_status, expected",
    (
        (None, False),
        (UserStatus.USER, False),
        (UserStatus.EDITOR, True),
        (UserStatus.ADMIN, True),
    )
)
def test_can_access(
        user_status: UserStatus | None,
        expected: bool
):
    result = can_access(user_status, min_status=UserStatus.EDITOR)
    assert result == expected


def test_user_status_checker_unauthorized():
    checker = UserStatusChecker(min_status=UserStatus.EDITOR)

    with pytest.raises(UnauthorizedError):
        checker(user_status=None)


def test_user_status_checker_no_access():
    checker = UserStatusChecker(min_status=UserStatus.EDITOR)

    with pytest.raises(LowStatusError):
        checker(user_status=UserStatus.USER)


@pytest.mark.parametrize(
    "user_status",
    (
        (UserStatus.EDITOR,),
        (UserStatus.ADMIN,),
    )
)
def test_user_status_checker_have_access(user_status: tuple[UserStatus]):
    checker = UserStatusChecker(min_status=UserStatus.EDITOR)

    # Not raises
    checker(user_status=user_status[0])
