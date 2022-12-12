from sqlalchemy import select

from auth.utils import hash_password
from infrastructure.db import BaseRepository, User
from users.dto import UserDBInsertDTO, UserDBUpdateDTO


class UserRepository(BaseRepository[User, UserDBInsertDTO, UserDBUpdateDTO]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        user = await self.db.scalars(
            select(User)
            .where(User.email == email.lower())
        )
        return user.first()

    # noinspection PyShadowingBuiltins
    async def update(self, id: int, update_dto: UserDBUpdateDTO) -> User:
        if update_dto.password is not None:
            update_dto.password = hash_password(
                id, update_dto.password
            )
        return await super().update(id, update_dto)

    async def insert(self, insert_dto: UserDBInsertDTO) -> User:
        result = await super().insert(insert_dto)
        return await self.update(
            result.id,
            UserDBUpdateDTO(password=insert_dto.password)
        )
