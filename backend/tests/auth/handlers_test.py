from unittest.mock import Mock

from httpx import AsyncClient

from auth.dto import LoginInputDTO
from common.cookie import ProjectCookies
from infrastructure.db import User


async def test_login_success(
        test_client: AsyncClient,
        redis_override: Mock,
        user_admin_in_db: User,
):
    response = await test_client.post(
        '/api/auth/login',
        json=LoginInputDTO(
            email=user_admin_in_db.email,
            password='password'
        ).dict()
    )
    body = response.json()
    session_id = response.cookies[ProjectCookies.SESSION_ID]
    session_in_db = redis_override.get(session_id)

    assert body['id'] == user_admin_in_db.id
    assert session_in_db


async def test_logout_success(
        test_client: AsyncClient,
        redis_override: Mock,
        user_admin_in_db: User,
):
    redis_override.set('user_session:123', user_admin_in_db.id)
    response = await test_client.delete(
        '/api/auth/logout',
        cookies={
            'session_id': '123'
        }
    )
    assert 'session_id=""' in response.headers['set-cookie']
    assert await redis_override.get('user_session:123') is None
