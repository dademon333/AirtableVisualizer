from httpx import AsyncClient

from entity_type_connections.dto import CreateTypeConnectionInputDTO, \
    UpdateTypeConnectionInputDTO, EntityTypeConnectionDBInsertDTO
from entity_type_connections.exceptions import TypeConnectionNotFoundResponse
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import EntityTypeConnection, EntityConnection, \
    EntityType


async def test_list_connections_success(
        entity_type_connection_list_in_db: list[EntityTypeConnection],
        test_client: AsyncClient,
):
    result = await test_client.get(
        '/api/type_connections/list'
    )
    assert len(result.json()) == len(entity_type_connection_list_in_db)


async def test_get_all_connections_success(
        entity_type_connection_repository: EntityTypeConnectionRepository,
        entity_connection_list_in_db: list[EntityConnection],
        entity_type_connection_list: list[EntityTypeConnection],
        test_client: AsyncClient,
):
    await entity_type_connection_repository.bulk_insert(
        [
            EntityTypeConnectionDBInsertDTO.from_orm(x)
            for x in entity_type_connection_list[1:]
        ]
    )

    result = await test_client.get('/api/type_connections/all')
    result = result.json()

    result_entity_connections: list[EntityConnection] = sum(
        [x['entity_connections'] for x in result.values()],
        []
    )

    assert len(result) > 0
    assert len(result) == len(entity_type_connection_list)
    assert len(result_entity_connections) == len(entity_connection_list_in_db)


async def test_get_connection_info_success(
        test_client: AsyncClient,
        entity_connection_in_db: EntityConnection,
):
    result = await test_client.get(
        f'/api/type_connections/{entity_connection_in_db.id}'
    )
    result = result.json()

    assert result['id'] == entity_connection_in_db.type_connection_id
    assert result['entity_connections'][0]['id'] == entity_connection_in_db.id


async def test_get_connection_info_not_found(
        test_client: AsyncClient,
        admin_status_request: None,
):
    result = await test_client.get(
        f'/api/type_connections/123'
    )
    assert result.status_code == 404
    assert result.json()['detail'] == TypeConnectionNotFoundResponse().detail


async def test_create_connection_success(
        entity_type_connection_repository: EntityTypeConnectionRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    result = await test_client.post(
        f'/api/type_connections',
        json=CreateTypeConnectionInputDTO(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME,
            parent_column_name='Курс',
            child_column_name='Темы',
        ).dict()
    )
    result = result.json()

    connection = await entity_type_connection_repository.get_by_id(
        id=result['id']
    )
    assert connection.parent_type == EntityType.COURSE
    assert connection.child_type == EntityType.THEME
    assert connection.parent_column_name == 'Курс'
    assert connection.child_column_name == 'Темы'


async def test_update_column_name_success(
        entity_type_connection_in_db: EntityTypeConnection,
        entity_type_connection_repository: EntityTypeConnectionRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    result = await test_client.put(
        f'/api/type_connections/{entity_type_connection_in_db.id}',
        json=UpdateTypeConnectionInputDTO(
            parent_column_name='foo',
            child_column_name='bar',
        ).dict()
    )
    result = result.json()

    connection = await entity_type_connection_repository.get_by_id(
        id=result['id']
    )
    assert connection.parent_type == EntityType.COURSE
    assert connection.child_type == EntityType.THEME
    assert connection.parent_column_name == 'foo'
    assert connection.child_column_name == 'bar'


async def test_delete_connection_success(
        entity_type_connection_in_db: EntityTypeConnection,
        entity_type_connection_repository: EntityTypeConnectionRepository,
        test_client: AsyncClient,
        admin_status_request: None,
):
    await test_client.delete(
        f'/api/type_connections/{entity_type_connection_in_db.id}'
    )

    connection = await entity_type_connection_repository.get_by_id(
        id=entity_type_connection_in_db.id
    )
    assert connection is None
