from courses.modules import get_connectivity_component
from db import EntityType, EntitiesTypesConnection


def test_no_connections():
    connections = []
    expected = [EntityType.COURSE]
    result = get_connectivity_component(connections)
    assert result == expected


def test_one_connection():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        )
    ]
    expected = [EntityType.COURSE, EntityType.THEME]
    result = get_connectivity_component(connections)
    assert result == expected


def test_linear_connectivity_component():
    connections = [
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
            child_type=EntityType.COMPETENCE
        )
    ]
    expected = [
        EntityType.COURSE,
        EntityType.THEME,
        EntityType.KNOWLEDGE,
        EntityType.COMPETENCE
    ]
    result = get_connectivity_component(connections)
    assert result == expected


def test_with_branch():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.THEME,
            child_type=EntityType.KNOWLEDGE
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.TASK
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.TASK,
            child_type=EntityType.KNOWLEDGE
        )
    ]
    expected = [
        EntityType.COURSE,
        EntityType.THEME,
        EntityType.KNOWLEDGE,
        EntityType.QUANTUM,
        EntityType.TASK
    ]
    result = get_connectivity_component(connections)
    assert result == expected


def test_two_components():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.THEME,
            child_type=EntityType.KNOWLEDGE
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.METRIC,
            child_type=EntityType.TARGET
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.TARGET,
            child_type=EntityType.TASK
        )
    ]
    expected = [
        EntityType.COURSE,
        EntityType.THEME,
        EntityType.KNOWLEDGE
    ]
    result = get_connectivity_component(connections)
    assert result == expected
