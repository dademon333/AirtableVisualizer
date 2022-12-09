from httpx import AsyncClient

from common.responses import OkResponse
from entity_connections.dto import EntityConnectionInputDTO
from entity_connections.exceptions import EntityConnectionNotFoundResponse
from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import Entity, EntityConnection


async def test_connect_entities_success(
        entity_theme_in_db: Entity,
        entity_course_in_db: Entity,
        entity_type_connection_in_db: Entity,
        entity_connection_repository: EntityConnectionRepository,
        test_client: AsyncClient,
        editor_status_request: None,
):
    result = await test_client.post(
        '/api/entity_connections',
        json=EntityConnectionInputDTO(
            parent_id=entity_course_in_db.id,
            child_id=entity_theme_in_db.id,
        ).dict()
    )
    connect_in_db = await entity_connection_repository.get_by_id(
        result.json()['id']
    )
    assert connect_in_db


async def test_disconnect_entities_success(
        entity_connection_in_db: EntityConnection,
        entity_connection_repository: EntityConnectionRepository,
        test_client: AsyncClient,
        editor_status_request: None,
):
    result = await test_client.delete(
        f'/api/entity_connections/{entity_connection_in_db.id}'
    )
    assert result.status_code == 200
    assert result.json() == OkResponse()


async def test_disconnect_entities_not_found(
        test_client: AsyncClient,
        editor_status_request: None,
):
    result = await test_client.delete('/api/entity_connections/123')
    assert result.status_code == 404
    assert result.json()['detail'] == EntityConnectionNotFoundResponse().detail
