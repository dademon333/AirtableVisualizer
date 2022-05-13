from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import Entity, EntityType
from common.schemas.entities import EntityCreate, EntityUpdate
from .base import CRUDBase


class CRUDEntities(CRUDBase[Entity, EntityCreate, EntityUpdate]):
    @staticmethod
    async def get_by_type(
            db: AsyncSession,
            entity_type: EntityType,
            limit: int = 500,
            offset: int = 0
    ) -> list[Entity]:
        result = await db.scalars(
            select(Entity)
            .where(Entity.type == entity_type)
            .order_by(Entity.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()

    @staticmethod
    async def search_by_name(
            db: AsyncSession,
            entity_type: EntityType,
            query: str,
            limit: int = 500,
            offset: int = 0
    ) -> list[Entity]:
        query = query.replace('%', r'\%').replace('*', r'\*')
        query = f'%{query}%'
        result = await db.scalars(
            select(Entity)
            .where(
                (Entity.type == entity_type)
                & (Entity.name.ilike(query))  # noqa
            )
            .order_by(Entity.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()


entities = CRUDEntities(Entity)
