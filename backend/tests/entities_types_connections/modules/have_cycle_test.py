import pytest

from db import EntitiesTypesConnection, EntityType
from entities_types_connections.modules import have_cycle


@pytest.mark.parametrize(
    'connections',
    [
        [
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.THEME
            ),
        ]
    ]
)
def test_cleans_self_referenced(connections):
    assert not have_cycle(connections)


@pytest.mark.parametrize(
    'connections',
    [
        [
             EntitiesTypesConnection(
                 parent_type=EntityType.COURSE,
                 child_type=EntityType.THEME
             )
        ],
        [
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            )
        ],
        [
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.COMPETENCE
            )
        ],
        [
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.KNOWLEDGE
            ),
        ],
    ]
)
def test_no_cycle(connections):
    assert not have_cycle(connections)


@pytest.mark.parametrize(
    'connections',
    [
        [
             EntitiesTypesConnection(
                 parent_type=EntityType.COURSE,
                 child_type=EntityType.THEME
             ),
             EntitiesTypesConnection(
                 parent_type=EntityType.THEME,
                 child_type=EntityType.KNOWLEDGE
             ),
             EntitiesTypesConnection(
                 parent_type=EntityType.KNOWLEDGE,
                 child_type=EntityType.COURSE
             ),
        ],
        [
            EntitiesTypesConnection(
                parent_type=EntityType.COURSE,
                child_type=EntityType.THEME
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.TARGET
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.THEME,
                child_type=EntityType.KNOWLEDGE
            ),
            EntitiesTypesConnection(
                parent_type=EntityType.KNOWLEDGE,
                child_type=EntityType.COURSE
            ),
        ]
    ]
)
def test_have_cycle(connections):
    assert have_cycle(connections)
