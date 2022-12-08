from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import get_db


def get_entity_type_connection_repository(
        db: AsyncSession = Depends(get_db),
) -> EntityTypeConnectionRepository:
    return EntityTypeConnectionRepository(db)
