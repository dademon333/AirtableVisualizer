from sqlalchemy import select

from entities.dto import EntityDBInsertDTO, EntityDBUpdateDTO
from infrastructure.db import BaseRepository, Entity, EntityType


class EntityRepository(
    BaseRepository[Entity, EntityDBInsertDTO, EntityDBUpdateDTO]
):
    model = Entity

    async def list_by_type(
            self,
            entity_type: EntityType,
            limit: int = 250,
            offset: int = 0
    ) -> list[Entity]:
        result = await self.db.scalars(
            select(Entity)
            .where(Entity.type == entity_type)
            .order_by(Entity.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()

    async def search_by_name(
            self,
            query: str,
            entity_type: EntityType | None = None,
            limit: int = 250,
            offset: int = 0
    ) -> list[Entity]:
        query = query.replace('%', r'\%').replace('*', r'\*')
        query = f'%{query}%'

        type_condition = Entity.type == entity_type if entity_type else True
        result = await self.db.scalars(
            select(Entity)
            .where(Entity.name.ilike(query) & type_condition)
            .order_by(Entity.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()
