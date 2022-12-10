from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from entities.exceptions import EntityNotFoundError
from entities.repository import EntityRepository
from entity_connections.dto import EntityConnectionInputDTO
from entity_connections.exceptions import EntityConnectionAlreadyExistsError
from entity_connections.repository import EntityConnectionRepository
from entity_connections.use_cases.connect_entities import \
    ConnectEntitiesUseCase
from entity_type_connections.exceptions import TypeConnectionNotFoundError
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import Entity, EntityTypeConnection, EntityConnection


@pytest.fixture()
def use_case() -> ConnectEntitiesUseCase:
    return ConnectEntitiesUseCase(
        entity_repository=Mock(spec=EntityRepository),
        entity_connection_repository=Mock(spec=EntityConnectionRepository),
        entity_type_connection_repository=Mock(
            spec=EntityTypeConnectionRepository
        ),
    )


@pytest.fixture()
def input_dto(
        entity_course: Entity,
        entity_theme: Entity,
) -> EntityConnectionInputDTO:
    return EntityConnectionInputDTO(
        parent_id=entity_course.id,
        child_id=entity_theme.id,
    )


async def test_parent_not_exists(
        entity_course: Entity,
        input_dto: EntityConnectionInputDTO,
        use_case: ConnectEntitiesUseCase,
):
    use_case.entity_repository.get_by_id = CoroutineMock(
        side_effect=[entity_course, None]
    )

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(input_dto)


async def test_type_connection_not_exists(
        entity_course: Entity,
        entity_theme: Entity,
        input_dto: EntityConnectionInputDTO,
        use_case: ConnectEntitiesUseCase,
):
    use_case.entity_repository.get_by_id = CoroutineMock(
        side_effect=[entity_course, entity_theme]
    )
    use_case.entity_type_connection_repository.get_by_types = CoroutineMock(
        return_value=None
    )

    with pytest.raises(TypeConnectionNotFoundError):
        await use_case.execute(input_dto)


async def test_connection_already_exists(
        entity_course: Entity,
        entity_theme: Entity,
        entity_type_connection: EntityTypeConnection,
        entity_connection: EntityConnection,
        input_dto: EntityConnectionInputDTO,
        use_case: ConnectEntitiesUseCase,
):
    use_case.entity_repository.get_by_id = CoroutineMock(
        side_effect=[entity_course, entity_theme]
    )
    use_case.entity_type_connection_repository.get_by_types = CoroutineMock(
        return_value=entity_type_connection
    )
    use_case.entity_connection_repository.get_by_entities = CoroutineMock(
        return_value=entity_connection
    )

    with pytest.raises(EntityConnectionAlreadyExistsError):
        await use_case.execute(input_dto)
