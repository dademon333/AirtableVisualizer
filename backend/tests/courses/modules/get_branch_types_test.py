from courses.modules import get_dependent_branch_types
from db import EntitiesTypesConnection, EntityType


def test_one_type():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.KNOWLEDGE,
            child_type=EntityType.THEME
        )
    ]
    expected = [EntityType.KNOWLEDGE]
    result = get_dependent_branch_types(EntityType.KNOWLEDGE, connections)
    assert set(result) == set(expected)


def test_two_types():
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
    expected = [EntityType.QUANTUM, EntityType.KNOWLEDGE]
    result = get_dependent_branch_types(EntityType.QUANTUM, connections)
    assert set(result) == set(expected)


def test_tree_form_branch():
    connections = [
        EntitiesTypesConnection(
            parent_type=EntityType.COURSE,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.THEME
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.KNOWLEDGE
        )
    ]
    expected = [EntityType.QUANTUM, EntityType.KNOWLEDGE]
    result = get_dependent_branch_types(EntityType.QUANTUM, connections)
    assert set(result) == set(expected)


def test_large_tree_form_branch():
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
            child_type=EntityType.SKILL
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.SKILL,
            child_type=EntityType.THEME
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.KNOWLEDGE,
            child_type=EntityType.COMPETENCE
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.COMPETENCE,
            child_type=EntityType.PROFESSION
        ),
    ]
    expected = [
        EntityType.QUANTUM,
        EntityType.KNOWLEDGE,
        EntityType.SKILL,
        EntityType.COMPETENCE,
        EntityType.PROFESSION
    ]
    result = get_dependent_branch_types(EntityType.QUANTUM, connections)
    assert set(result) == set(expected)


def test_bridge_branch():
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
            parent_type=EntityType.COURSE,
            child_type=EntityType.TARGET
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.TARGET,
            child_type=EntityType.TASK
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.SKILL
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.SKILL,
            child_type=EntityType.KNOWLEDGE
        ),

        EntitiesTypesConnection(
            parent_type=EntityType.QUANTUM,
            child_type=EntityType.COMPETENCE
        ),
        EntitiesTypesConnection(
            parent_type=EntityType.COMPETENCE,
            child_type=EntityType.TASK
        ),

    ]
    expected = [
        EntityType.QUANTUM,
        EntityType.SKILL,
        EntityType.COMPETENCE
    ]
    result = get_dependent_branch_types(EntityType.QUANTUM, connections)
    assert set(result) == set(expected)
