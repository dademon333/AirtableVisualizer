from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from users.repository import UserRepository
from users.use_cases.create_user import CreateUserUseCase
from users.use_cases.delete_user import DeleteUserUseCase
from users.use_cases.get_user import GetUserUseCase
from users.use_cases.list_users import ListUsersUseCase
from users.use_cases.update_user import UpdateUserUseCase


def get_user_repository(
        db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db=db)


def get_list_users_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
) -> ListUsersUseCase:
    return ListUsersUseCase(user_repository)


def get_get_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserUseCase:
    return GetUserUseCase(user_repository)


def get_create_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def get_update_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repository)


def get_delete_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repository)
