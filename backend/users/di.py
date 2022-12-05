from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from users.repository import UserRepository


def get_user_repository(
        db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db=db)
