from httpx import AsyncClient

from entities.dto import EntityDBInsertDTO, EntityOutputDTO
from entities.exceptions import EntityNotFoundResponse
from entities.repository import EntityRepository
from infrastructure.db import EntityType, Entity


async def test_get_entity_success(
        test_client: AsyncClient,
        entity_course_in_db: Entity,
):
    response = await test_client.get(f'/api/entities/{entity_course_in_db.id}')
    assert response.json()['id'] == entity_course_in_db.id


async def test_get_entity_not_found(test_client: AsyncClient):
    response = await test_client.get(f'/api/entities/1')
    assert response.status_code == 404
    assert response.json() == EntityNotFoundResponse().dict()


async def test_list_entities_success(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
):
    course = EntityType.COURSE.value
    response = await test_client.get(f'/api/entities/list/{course}')
    assert len(response.json()) == len(entity_course_list_in_db)


async def test_search_entities_all_types(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
):
    # Search by one russian letter 'а'
    response = await test_client.get(
        '/api/entities/search',
        params={'query': 'а'}
    )
    response = response.json()
    assert len(set(x['type'] for x in response)) > 1


async def test_search_entities_specific_type(
        test_client: AsyncClient,
        entity_course_list_in_db: list[Entity],
        entity_theme_list_in_db: list[Entity],
):
    # Search by one russian letter 'а'
    response = await test_client.get(
        '/api/entities/search',
        params={'query': 'а', 'entity_type': EntityType.COURSE.value}
    )
    response = response.json()
    assert set(x['type'] for x in response) == {EntityType.COURSE.value}


async def test_create_entity_success(
        entity_course: Entity,
        test_client: AsyncClient,
        editor_status_request: None,
):
    response = await test_client.post(
        '/api/entities',
        json=EntityDBInsertDTO.from_orm(entity_course).dict(exclude_unset=True)
    )
    response = EntityOutputDTO(**response.json())
    assert response.type == entity_course.type
    assert response.name == entity_course.name


async def test_update_entity_success(
        entity_course_in_db: Entity,
        test_client: AsyncClient,
        editor_status_request: None,
):
    response = await test_client.put(
        f'/api/entities/{entity_course_in_db.id}',
        json={'name': 'new name'}
    )
    response = response.json()
    assert response['name'] == 'new name'
    assert response['id'] == entity_course_in_db.id
    assert response['description'] == entity_course_in_db.description


async def test_update_entity_not_found(
        test_client: AsyncClient,
        editor_status_request: None,
):
    response = await test_client.put(
        f'/api/entities/{100}',
        json={'name': 'new name'}
    )
    assert response.status_code == 404
    assert response.json() == EntityNotFoundResponse().dict()


async def test_delete_entity_success(
        test_client: AsyncClient,
        entity_repository: EntityRepository,
        entity_course_in_db: Entity,
        editor_status_request: None,
):
    response = await test_client.delete(
        f'/api/entities/{entity_course_in_db.id}',
    )
    assert response.status_code == 200
    assert await entity_repository.get_by_id(entity_course_in_db.id) is None
