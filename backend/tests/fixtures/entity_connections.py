import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from entity_connections.dto import EntityConnectionDBInsertDTO
from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import EntityConnection, EntityTypeConnection, Entity


@pytest.fixture()
def entity_connection_repository(
        db: AsyncSession,
) -> EntityConnectionRepository:
    return EntityConnectionRepository(db)


@pytest.fixture()
def entity_connection(
        entity_course: Entity,
        entity_theme: Entity,
        entity_type_connection: EntityTypeConnection,
) -> EntityConnection:
    return EntityConnection(
        id=1,
        parent_id=entity_course.id,
        child_id=entity_theme.id,
        type_connection_id=entity_type_connection.id
    )


@pytest.fixture()
async def entity_connection_in_db(
        entity_course_in_db: Entity,
        entity_theme_in_db: Entity,
        entity_type_connection_in_db: EntityTypeConnection,
        entity_connection: EntityConnection,
        entity_connection_repository: EntityConnectionRepository,
) -> EntityConnection:
    await entity_connection_repository.insert(
        EntityConnectionDBInsertDTO.from_orm(entity_connection)
    )
    return entity_connection
