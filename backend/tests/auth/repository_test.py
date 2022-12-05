from unittest.mock import Mock

import pytest

from auth.repository import AuthRepository


@pytest.fixture()
def repository(redis_mock: Mock) -> AuthRepository:
    return AuthRepository(redis_client=redis_mock)


async def test_get_user_id_by_token_no_session(repository: AuthRepository):
    result = await repository.get_user_id_by_token(access_token="abc")
    assert result is None


async def test_get_user_id_by_token_success(
        repository: AuthRepository,
        redis_mock: Mock
):
    redis_mock.set("user_token:abc", "1")
    result = await repository.get_user_id_by_token(access_token="abc")
    assert result == 1


async def test_create_session(
        repository: AuthRepository,
        redis_mock: Mock
):
    access_token = await repository.create_session(user_id=123)
    assert access_token
    assert redis_mock.get(f"user_token:{access_token}")


async def test_delete_session(
        repository: AuthRepository,
        redis_mock: Mock
):
    redis_mock.set(key="user_token:abc", value=123)
    await repository.delete_session(access_token="abc")
    assert await redis_mock.get(key="user_token:abc") is None
