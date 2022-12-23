from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from auth.dto import LoginInputDTO
from auth.exceptions import LoginError
from auth.repository import AuthRepository
from auth.use_cases.login import LoginUseCase
from infrastructure.db import User
from users.repository import UserRepository


@pytest.fixture()
def use_case() -> LoginUseCase:
    return LoginUseCase(
        auth_repository=Mock(spec=AuthRepository),
        user_repository=Mock(spec=UserRepository),
    )


@pytest.fixture()
def input_dto() -> LoginInputDTO:
    return LoginInputDTO(
        email='user@example.com',
        password='password',
    )


async def test_user_not_exists(
        use_case: LoginUseCase,
        input_dto: LoginInputDTO
):
    use_case.user_repository.get_by_email = CoroutineMock(
        return_value=None
    )

    with pytest.raises(LoginError):
        await use_case.execute(input_dto)


async def test_wrong_password(
        use_case: LoginUseCase,
        input_dto: LoginInputDTO,
        user: User,
):
    user.password = '123'
    use_case.user_repository.get_by_email = CoroutineMock(
        return_value=user
    )

    with pytest.raises(LoginError):
        await use_case.execute(input_dto)


async def test_success(
        use_case: LoginUseCase,
        input_dto: LoginInputDTO,
        user: User,
):
    use_case.user_repository.get_by_email = CoroutineMock(
        return_value=user
    )
    use_case.auth_repository.create_session = CoroutineMock(
        return_value='123'
    )

    response = await use_case.execute(input_dto)
    assert response.access_token == '123'
