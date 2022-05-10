from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Entity, EntityType
from schemas.entities import EntityCreate, EntityUpdate
from .base import CRUDBase


class CRUDEntities(CRUDBase[Entity, EntityCreate, EntityUpdate]):
    # noinspection PyShadowingBuiltins
    async def get_by_type(
            self,
            db: AsyncSession,
            type: EntityType,
            limit: int = 500,
            offset: int = 0
    ):
        result = await db.scalars(
            select(Entity)
            .where(Entity.type == type)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()


entities = CRUDEntities(Entity)
