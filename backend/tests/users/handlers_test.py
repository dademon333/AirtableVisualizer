from typing import NoReturn, Callable

from httpx import AsyncClient

from auth.utils import hash_password
from infrastructure.db import User
from users.dto import UserOutputDTO, CreateUserInputDTO, UserSelfUpdateInputDTO
from users.exceptions import UserEmailAlreadyUsedResponse, UserNotFoundResponse
from users.repository import UserRepository


async def test_list_users_success(
        user_in_db: User,
        user_admin_in_db: User,
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.get('/api/users/list')
    assert len(response.json()) == 2


async def test_get_self_info_success(
        user_in_db: User,
        override_get_user_id: Callable[[int], NoReturn],
        test_client: AsyncClient,
):
    override_get_user_id(user_in_db.id)
    response = await test_client.get('/api/users/me')
    response = UserOutputDTO.parse_obj(response.json())
    assert response.id == user_in_db.id
    assert response.email == user_in_db.email


async def test_get_user_success(
        user_in_db: User,
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.get(f'/api/users/{user_in_db.id}')
    response = UserOutputDTO.parse_obj(response.json())
    assert response.id == user_in_db.id
    assert response.email == user_in_db.email


async def test_get_user_not_found(
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.get(f'/api/users/123')
    assert response.status_code == 404
    assert response.json()['detail'] == UserNotFoundResponse().detail


async def test_create_user_success(
        user: User,
        user_repository: UserRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    user.password = 'password'
    input_dto = CreateUserInputDTO.from_orm(user)
    response = await test_client.post('/api/users', json=input_dto.dict())

    user_in_db = await user_repository.get_by_id(response.json()['id'])
    assert user_in_db.email == user.email
    assert user_in_db.name == user.name
    assert user_in_db.status == user.status
    assert user_in_db.password == hash_password(user_in_db.id, 'password')


async def test_create_user_email_already_used(
        user_in_db: User,
        user_repository: UserRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.post(
        '/api/users',
        json=CreateUserInputDTO.from_orm(user_in_db).dict()
    )
    assert response.status_code == 409
    assert response.json()['detail'] == UserEmailAlreadyUsedResponse().detail


async def test_update_self_success(
        user_in_db: User,
        test_client: AsyncClient,
        override_get_user_id: Callable[[int], NoReturn]
):
    override_get_user_id(user_in_db.id)
    response = await test_client.put(
        '/api/users/me',
        json=UserSelfUpdateInputDTO(name='new name').dict(exclude_unset=True)
    )
    response = response.json()
    assert response['name'] == 'new name'
    assert response['email'] == user_in_db.email


async def test_update_self_email_exists(
        user_in_db: User,
        user_admin_in_db: User,
        test_client: AsyncClient,
        override_get_user_id: Callable[[int], NoReturn]
):
    override_get_user_id(user_in_db.id)
    response = await test_client.put(
        '/api/users/me',
        json=UserSelfUpdateInputDTO(email=user_admin_in_db.email).dict()
    )
    assert response.status_code == 409
    assert response.json()['detail'] == UserEmailAlreadyUsedResponse().detail


async def test_update_user_success(
        user_in_db: User,
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.put(
        f'/api/users/{user_in_db.id}',
        json=UserSelfUpdateInputDTO(name='new name').dict(exclude_unset=True)
    )
    response = response.json()
    assert response['name'] == 'new name'
    assert response['email'] == user_in_db.email


async def test_delete_user_success(
        user_in_db: User,
        user_repository: UserRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.delete(f'/api/users/{user_in_db.id}')
    assert response.status_code == 200
    assert await user_repository.get_by_id(user_in_db.id) is None


async def test_delete_user_not_found(
        test_client: AsyncClient,
        admin_status_request: None,
):
    response = await test_client.delete(f'/api/users/123')
    assert response.status_code == 404
    assert response.json()['detail'] == UserNotFoundResponse().detail
