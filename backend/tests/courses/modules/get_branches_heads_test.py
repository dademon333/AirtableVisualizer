from courses.modules import get_dependent_branches_heads
from db import EntitiesTypesConnection, EntityType


def test_no_heads():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        )
    ]
    expected = []
    result = get_dependent_branches_heads(connections)
    assert set(result) == set(expected)


def test_one_head():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.KNOWLEDGE
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.KNOWLEDGE,
            child_type=EntityType.THEME
        )
    ]
    expected = [EntityType.QUANTUM]
    result = get_dependent_branches_heads(connections)
    assert set(result) == set(expected)


def test_two_heads():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.KNOWLEDGE
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.KNOWLEDGE,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.SUOS_COMPETENCE,
            child_type=EntityType.COMPETENCE
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.COMPETENCE,
            child_type=EntityType.THEME
        )
    ]
    expected = [EntityType.QUANTUM, EntityType.SUOS_COMPETENCE]
    result = get_dependent_branches_heads(connections)
    assert set(result) == set(expected)
