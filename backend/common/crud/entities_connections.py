from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import EntitiesConnection
from common.schemas.entities_connections import EntitiesConnectionCreate, EntitiesConnectionUpdate
from .base import CRUDBase


class CRUDEntitiesConnections(CRUDBase[EntitiesConnection, EntitiesConnectionCreate, EntitiesConnectionUpdate]):
    @staticmethod
    async def get_by_entity_id(
            db: AsyncSession,
            entity_id: int
    ) -> list[EntitiesConnection]:
        result = await db.scalars(
            select(EntitiesConnection)
            .where(
                (EntitiesConnection.parent_id == entity_id)
                | (EntitiesConnection.child_id == entity_id)
            )
        )
        return result.unique().all()

    @staticmethod
    async def get_by_entities(
            db: AsyncSession,
            parent_id: int,
            child_id: int
    ) -> EntitiesConnection | None:
        result = await db.scalars(
            select(EntitiesConnection)
            .where(
                (EntitiesConnection.parent_id == parent_id)
                & (EntitiesConnection.child_id == child_id)
            )
        )
        return result.first()


entities_connections = CRUDEntitiesConnections(EntitiesConnection)
