from sqlalchemy import select

from auth.utils import hash_password
from infrastructure.db import BaseRepository, User
from users.dto import UserInsertDTO, UserUpdateDTO


class UserRepository(BaseRepository[User, UserInsertDTO, UserUpdateDTO]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        user = await self.db.scalars(
            select(User)
            .where(User.email == email.lower())
        )
        return user.first()

    # noinspection PyShadowingBuiltins
    async def update(self, id: int, update_dto: UserUpdateDTO) -> User:
        if update_dto.password is not None:
            update_dto.password = hash_password(
                id, update_dto.password
            )
        return await super().update(id, update_dto)

    async def insert(self, insert_dto: UserInsertDTO) -> User:
        result = await super().insert(insert_dto)
        return await self.update(
            result.id,
            UserUpdateDTO(password=insert_dto.password)
        )
