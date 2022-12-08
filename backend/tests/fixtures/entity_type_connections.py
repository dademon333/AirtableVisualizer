import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from entity_type_connections.dto import EntityTypeConnectionDBInsertDTO
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import EntityTypeConnection, EntityType


@pytest.fixture()
def entity_type_connection_repository(
        db: AsyncSession,
) -> EntityTypeConnectionRepository:
    return EntityTypeConnectionRepository(db)


@pytest.fixture
def entity_type_connection() -> EntityTypeConnection:
    return EntityTypeConnection(
        id=1,
        parent_type=EntityType.COURSE,
        child_type=EntityType.THEME,
    )


@pytest.fixture
async def entity_type_connection_in_db(
        entity_type_connection_repository: EntityTypeConnectionRepository,
        entity_type_connection: EntityTypeConnection,
) -> EntityTypeConnection:
    await entity_type_connection_repository.insert(
        EntityTypeConnectionDBInsertDTO.from_orm(entity_type_connection)
    )
    return entity_type_connection
