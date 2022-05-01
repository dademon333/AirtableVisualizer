from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud.base import CRUDBase
from db import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        user = await db.scalars(
            select(User).
            where(User.email == email)
        )
        return user.first()


user = CRUDUser(User)
