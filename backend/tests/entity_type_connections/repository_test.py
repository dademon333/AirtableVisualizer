import pytest

from entity_type_connections.dto import EntityTypeConnectionDBInsertDTO
from entity_type_connections.exceptions import TypeConnectionAlreadyExistsError
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import EntityTypeConnection, EntityType


async def test_get_by_types_success(
        entity_type_connection_in_db: EntityTypeConnection,
        entity_type_connection_repository: EntityTypeConnectionRepository,
):
    result = await entity_type_connection_repository.get_by_types(
        parent_type=entity_type_connection_in_db.parent_type,
        child_type=entity_type_connection_in_db.child_type,
    )
    assert result


async def test_get_by_types_reverse(
        entity_type_connection_in_db: EntityTypeConnection,
        entity_type_connection_repository: EntityTypeConnectionRepository,
):
    result = await entity_type_connection_repository.get_by_types(
        parent_type=entity_type_connection_in_db.child_type,
        child_type=entity_type_connection_in_db.parent_type,
    )
    assert result is None


async def test_insert_success(
        entity_type_connection_repository: EntityTypeConnectionRepository,
):
    result = await entity_type_connection_repository.insert(
        EntityTypeConnectionDBInsertDTO(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME,
        )
    )
    assert result


async def test_insert_already_exists(
        entity_type_connection_in_db: EntityTypeConnection,
        entity_type_connection_repository: EntityTypeConnectionRepository,
):
    with pytest.raises(TypeConnectionAlreadyExistsError):
        await entity_type_connection_repository.insert(
            EntityTypeConnectionDBInsertDTO.from_orm(
                entity_type_connection_in_db
            )
        )
