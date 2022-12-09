from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import EntityConnection


async def test_get_by_entity_id(
        entity_connection_in_db: EntityConnection,
        entity_connection_repository: EntityConnectionRepository,
):
    [result_by_child] = await entity_connection_repository.get_by_entity_id(
        entity_connection_in_db.parent_id
    )
    [result_by_parent] = await entity_connection_repository.get_by_entity_id(
        entity_connection_in_db.parent_id
    )
    assert result_by_child.id == result_by_parent.id \
           == entity_connection_in_db.id


async def test_get_by_entities(
        entity_connection_in_db: EntityConnection,
        entity_connection_repository: EntityConnectionRepository,
):
    result = await entity_connection_repository.get_by_entities(
        parent_id=entity_connection_in_db.parent_id,
        child_id=entity_connection_in_db.child_id,
    )
    assert result.id == entity_connection_in_db.id


async def test_get_by_entities_not_found(
        entity_connection_repository: EntityConnectionRepository,
):
    result = await entity_connection_repository.get_by_entities(
        parent_id=123,
        child_id=456,
    )
    assert result is None


async def test_get_by_type_connection(
        entity_connection_in_db: EntityConnection,
        entity_connection_repository: EntityConnectionRepository,
):
    result = await entity_connection_repository.get_by_type_connection(
        entity_connection_in_db.type_connection_id
    )
    assert result
