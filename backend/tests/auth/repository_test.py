from unittest.mock import Mock

import pytest

from auth.repository import AuthRepository


@pytest.fixture()
def repository(redis_mock: Mock) -> AuthRepository:
    return AuthRepository(redis_client=redis_mock)


async def test_get_user_id_by_session_no_session(repository: AuthRepository):
    result = await repository.get_user_id_by_session_id(session_id="abc")
    assert result is None


async def test_get_user_id_by_session_success(
        repository: AuthRepository,
        redis_mock: Mock
):
    redis_mock.set("user_session:abc", "1")
    result = await repository.get_user_id_by_session_id(session_id="abc")
    assert result == 1


async def test_create_session(
        repository: AuthRepository,
        redis_mock: Mock
):
    access_session = await repository.create_session(user_id=123)
    assert access_session
    assert redis_mock.get(f"user_session:{access_session}")


async def test_delete_session(
        repository: AuthRepository,
        redis_mock: Mock
):
    redis_mock.set(key="user_session:abc", value=123)
    await repository.delete_session(session_id="abc")
    assert await redis_mock.get(key="user_session:abc") is None
