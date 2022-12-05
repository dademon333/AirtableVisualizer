from auth.utils import hash_password
from infrastructure.db import User
from users.dto import UserUpdateDTO, UserInsertDTO
from users.repository import UserRepository


async def test_get_by_email_success(
        user_in_db: User,
        user_repository: UserRepository,
):
    assert await user_repository.get_by_email(user_in_db.email.upper())


async def test_update_hashes_password(
        user_in_db: User,
        user_repository: UserRepository,
):
    await user_repository.update(
        user_in_db.id,
        UserUpdateDTO(password="foobarbaz")
    )

    user_in_db = await user_repository.get_by_id(user_in_db.id)
    assert user_in_db.password == hash_password(user_in_db.id, "foobarbaz")


async def test_create_hashes_password(
        user: User,
        user_repository: UserRepository,
):
    user.password = "foobarbaz"
    await user_repository.insert(UserInsertDTO.from_orm(user))

    user_in_db = await user_repository.get_by_id(user.id)
    assert user_in_db.password == hash_password(user_in_db.id, "foobarbaz")
