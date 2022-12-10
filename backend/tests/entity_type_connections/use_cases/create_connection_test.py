from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock

from entity_type_connections.dto import CreateTypeConnectionInputDTO
from entity_type_connections.exceptions import \
    TypeConnectionAlreadyExistsError, TypeConnectionCreatesCycleError
from entity_type_connections.repository import EntityTypeConnectionRepository
from entity_type_connections.use_cases.create_connection import \
    CreateTypeConnectionUseCase
from infrastructure.db import EntityTypeConnection, EntityType


@pytest.fixture()
def use_case() -> CreateTypeConnectionUseCase:
    return CreateTypeConnectionUseCase(
        type_connection_repository=Mock(spec=EntityTypeConnectionRepository)
    )


async def test_connection_exists(
        entity_type_connection: EntityTypeConnection,
        use_case: CreateTypeConnectionUseCase,
):
    use_case.type_connection_repository.get_all = CoroutineMock(
        return_value=[entity_type_connection]
    )

    with pytest.raises(TypeConnectionAlreadyExistsError):
        await use_case.execute(
            CreateTypeConnectionInputDTO.from_orm(
                entity_type_connection
            )
        )


async def test_connection_creates_cycle(
        entity_type_connection: EntityTypeConnection,
        use_case: CreateTypeConnectionUseCase,
):
    use_case.type_connection_repository.get_all = CoroutineMock(
        return_value=[]
    )
    use_case.have_cycle = CoroutineMock(return_value=True)

    with pytest.raises(TypeConnectionCreatesCycleError):
        await use_case.execute(
            CreateTypeConnectionInputDTO.from_orm(
                entity_type_connection
            )
        )



@pytest.mark.parametrize(
    'connections',
    [
        [
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.THEME
            ),
        ]
    ]
)
def test_have_cycles_cleans_self_referenced(
        use_case: CreateTypeConnectionUseCase,
        connections: list[EntityTypeConnection]
):
    assert not use_case.have_cycle(connections)


@pytest.mark.parametrize(
    'connections',
    [
        [
             EntityTypeConnection(
                 parent_type=EntityType.COURSE,
                 child_type=EntityType.THEME
             )
        ],
        [
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            )
        ],
        [
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.COMPETENCE
            )
        ],
        [
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            ),
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.KNOWLEDGE
            ),
        ],
    ]
)
def test_have_cycle_no_cycle(
        use_case: CreateTypeConnectionUseCase,
        connections: list[EntityTypeConnection]
):
    assert not use_case.have_cycle(connections)


@pytest.mark.parametrize(
    'connections',
    [
        [
             EntityTypeConnection(
                 parent_type=EntityType.COURSE,
                 child_type=EntityType.THEME,
             ),
             EntityTypeConnection(
                 parent_type=EntityType.THEME,
                 child_type=EntityType.KNOWLEDGE,
             ),
             EntityTypeConnection(
                 parent_type=EntityType.KNOWLEDGE,
                 child_type=EntityType.COURSE,
             ),
        ],
        [
            EntityTypeConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME,
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.TARGET,
            ),
            EntityTypeConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE,
            ),
            EntityTypeConnection(
                parent_type=EntityType.KNOWLEDGE,
                child_type=EntityType.COURSE,
            ),
        ]
    ]
)
def test_have_cycle_have_cycle(
        use_case: CreateTypeConnectionUseCase,
        connections: list[EntityTypeConnection]
):
    assert use_case.have_cycle(connections)
