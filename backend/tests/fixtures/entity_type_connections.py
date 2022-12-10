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
def entity_type_connection_list() -> list[EntityTypeConnection]:
    return [
        EntityTypeConnection(
            id=1,
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME,
        ),
        EntityTypeConnection(
            id=2,
            parent_type=EntityType.THEME,
            child_type=EntityType.KNOWLEDGE,
        ),
        EntityTypeConnection(
            id=3,
            parent_type=EntityType.THEME,
            child_type=EntityType.THEME,
        ),
    ]


@pytest.fixture
async def entity_type_connection_in_db(
        entity_type_connection_repository: EntityTypeConnectionRepository,
        entity_type_connection: EntityTypeConnection,
) -> EntityTypeConnection:
    await entity_type_connection_repository.insert(
        EntityTypeConnectionDBInsertDTO.from_orm(entity_type_connection)
    )
    return entity_type_connection


@pytest.fixture
async def entity_type_connection_list_in_db(
        entity_type_connection_repository: EntityTypeConnectionRepository,
        entity_type_connection_list: list[EntityTypeConnection],
) -> list[EntityTypeConnection]:
    await entity_type_connection_repository.bulk_insert(
        [
            EntityTypeConnectionDBInsertDTO.from_orm(x)
            for x in entity_type_connection_list
        ]
    )
    return entity_type_connection_list
