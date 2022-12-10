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
def entity_connection_list(
        entity_course_list: Entity,
        entity_theme_list: Entity,
        entity_type_connection: EntityTypeConnection,
) -> list[EntityConnection]:
    themes_per_course = len(entity_theme_list) // len(entity_course_list)
    themes_chunks = [
        entity_theme_list[x:x + themes_per_course]
        for x in range(len(entity_course_list))
    ]

    id_ = 1
    result = []
    for course, themes in zip(entity_course_list, themes_chunks):
        for theme in themes:
            result.append(
                EntityConnection(
                    id=id_,
                    parent_id=course.id,
                    child_id=theme.id,
                    type_connection_id=entity_type_connection.id,
                )
            )
            id_ += 1

    return result


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


@pytest.fixture()
async def entity_connection_list_in_db(
        entity_course_list_in_db: Entity,
        entity_theme_list_in_db: Entity,
        entity_type_connection_in_db: EntityTypeConnection,
        entity_connection_list: list[EntityConnection],
        entity_connection_repository: EntityConnectionRepository,
) -> list[EntityConnection]:
    await entity_connection_repository.bulk_insert(
        [
            EntityConnectionDBInsertDTO.from_orm(x)
            for x in entity_connection_list
        ]
    )
    return entity_connection_list
