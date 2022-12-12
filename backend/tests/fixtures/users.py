from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import User, UserStatus
from users.dto import UserDBInsertDTO
from users.repository import UserRepository


@pytest.fixture()
def user_repository(db: AsyncSession) -> UserRepository:
    return UserRepository(db)


@pytest.fixture()
def user() -> User:
    return User(
        id=1,
        name='user',
        email='user@example.com',
        password='a9530fae5f0c2eed641f20b1f2514656'
                 'a8a5527752ca1d2e12c597ead98130b4',
        status=UserStatus.USER,
        created_at=datetime.fromisoformat('2022-10-10T00:00:00')
    )


@pytest.fixture()
def user_editor() -> User:
    return User(
        id=2,
        name='editor',
        email='editor@example.com',
        password='c893b50d34064516d796a9074f82a5cc'
                 'cf975c93749ac1de848687f7afa9bb37',
        status=UserStatus.EDITOR,
        created_at=datetime.fromisoformat('2022-10-10T00:00:00')
    )


@pytest.fixture()
def user_admin() -> User:
    return User(
        id=3,
        name='admin',
        email='admin@example.com',
        password='556caa5b5e69c3dce39abb6e399f2ebe'
                 '14fef5bf7635a77bdd39d79a8df2a1f7',
        status=UserStatus.ADMIN,
        created_at=datetime.fromisoformat('2022-10-10T00:00:00')
    )


@pytest.fixture()
async def user_in_db(user: User, user_repository: UserRepository) -> User:
    user.password = 'password|1'
    await user_repository.insert(UserDBInsertDTO.from_orm(user))
    return user


@pytest.fixture()
async def user_admin_in_db(
        user_admin: User,
        user_repository: UserRepository
) -> User:
    user_admin.password = f'password'
    await user_repository.insert(UserDBInsertDTO.from_orm(user_admin))
    return user_admin
