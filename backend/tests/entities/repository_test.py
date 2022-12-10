from entities.repository import EntityRepository
from entity_connections.dto import EntityConnectionDBInsertDTO
from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import Entity, EntityType, EntityConnection


async def test_get_by_type_success(
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_repository: EntityRepository,
):
    result = await entity_repository.get_by_type(EntityType.COURSE)
    assert len(result) == len(entity_course_list_in_db)


async def test_search_by_name_success(
        entity_course_list_in_db: list[Entity],
        entity_repository: EntityRepository,
):
    result = await entity_repository.search_by_name(
        entity_type=EntityType.COURSE,
        query=entity_course_list_in_db[0].name[2:5]
    )
    assert result


async def test_get_all_connected_no_connects(
        entity_course_list_in_db: list[Entity],
        entity_repository: EntityRepository,
):
    result = await entity_repository.get_all_connected()
    assert len(result) == 0



async def test_get_all_connected_two_connected(
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_type_connection_in_db: list[Entity],
        entity_connection: EntityConnection,
        entity_repository: EntityRepository,
        entity_connection_repository: EntityConnectionRepository,

):
    await entity_connection_repository.insert(
        EntityConnectionDBInsertDTO.from_orm(entity_connection)
    )
    result = await entity_repository.get_all_connected()
    assert len(result) == 2


async def test_get_all_connected_all_connected(
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_connection_list_in_db: list[EntityConnection],
        entity_repository: EntityRepository,
):
    result = await entity_repository.get_all_connected()
    assert len(result) == len(entity_connection_list_in_db) * 2
