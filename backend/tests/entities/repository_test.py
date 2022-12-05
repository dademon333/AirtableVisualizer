from entities.repository import EntityRepository
from infrastructure.db import Entity, EntityType


async def test_list_by_type_success(
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
        entity_repository: EntityRepository
):
    result = await entity_repository.list_by_type(EntityType.COURSE)
    assert len(result) == len(entity_course_list_in_db)


async def test_search_by_name_success(
        entity_course_list_in_db: list[Entity],
        entity_repository: EntityRepository
):
    result = await entity_repository.search_by_name(
        entity_type=EntityType.COURSE,
        query=entity_course_list_in_db[0].name[2:5]
    )
    assert result
