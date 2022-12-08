from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from entities.dto import EntityDBInsertDTO
from entities.repository import EntityRepository
from infrastructure.db import Entity, EntityType, EntitySize


@pytest.fixture()
def entity_repository(db: AsyncSession) -> EntityRepository:
    return EntityRepository(db)


@pytest.fixture()
def entity_course() -> Entity:
    return Entity(
        id=100,
        name='Математика',
        type=EntityType.COURSE,
        size=EntitySize.MEDIUM,
        description='Курс математики',
        study_time=216,
        created_at=datetime(2022, 10, 10, 16, 0, 0)
    )


@pytest.fixture()
def entity_theme() -> Entity:
    return Entity(
        id=200,
        name='Матрицы',
        type=EntityType.THEME,
        size=EntitySize.MEDIUM,
        description='Тема матриц',
        study_time=216,
        created_at=datetime(2022, 10, 10, 16, 0, 0)
    )


@pytest.fixture()
def entity_course_list() -> list[Entity]:
    return [
        Entity(
            id=100,
            name='Математика',
            type=EntityType.COURSE,
            size=EntitySize.MEDIUM,
            description='Курс математики',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
        Entity(
            id=101,
            name='Физика',
            type=EntityType.COURSE,
            size=EntitySize.MEDIUM,
            description='Курс физики',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
        Entity(
            id=102,
            name='История',
            type=EntityType.COURSE,
            size=EntitySize.MEDIUM,
            description='Курс истории',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
    ]


@pytest.fixture()
def entity_theme_list() -> list[Entity]:
    return [
        Entity(
            id=200,
            name='Матрицы',
            type=EntityType.THEME,
            size=EntitySize.MEDIUM,
            description='Тема матриц',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
        Entity(
            id=201,
            name='Механика',
            type=EntityType.THEME,
            size=EntitySize.MEDIUM,
            description='Тема механики',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
        Entity(
            id=202,
            name='Сталинградская битва',
            type=EntityType.THEME,
            size=EntitySize.MEDIUM,
            description='Тема сталинградской битвы',
            study_time=216,
            created_at=datetime(2022, 10, 10, 16, 0, 0)
        ),
    ]


@pytest.fixture()
async def entity_course_in_db(
        entity_course: Entity,
        entity_repository: EntityRepository
) -> Entity:
    await entity_repository.insert(EntityDBInsertDTO.from_orm(entity_course))
    return entity_course


@pytest.fixture()
async def entity_theme_in_db(
        entity_theme: Entity,
        entity_repository: EntityRepository
) -> Entity:
    await entity_repository.insert(EntityDBInsertDTO.from_orm(entity_theme))
    return entity_theme


@pytest.fixture()
async def entity_course_list_in_db(
        entity_course_list: list[Entity],
        entity_repository: EntityRepository
) -> list[Entity]:
    await entity_repository.bulk_insert(
        [EntityDBInsertDTO.from_orm(x) for x in entity_course_list]
    )
    return entity_course_list


@pytest.fixture()
async def entity_theme_list_in_db(
        entity_theme_list: list[Entity],
        entity_repository: EntityRepository
) -> list[Entity]:
    await entity_repository.bulk_insert(
        [EntityDBInsertDTO.from_orm(x) for x in entity_theme_list]
    )
    return entity_theme_list
