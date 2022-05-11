from enum import Enum

from common.db import EntitiesTypesConnection, EntityType


class Color(Enum):
    WHITE = 'white'
    GREY = 'grey'
    BLACK = 'black'


def _dfs(
        target: EntityType,
        descendants: dict[EntityType, list[EntityType]],
        colors: dict[EntityType, Color],
) -> bool:
    if colors[target] == Color.BLACK:
        return False
    if colors[target] == Color.GREY:
        return True

    colors[target] = Color.GREY
    for child in descendants[target]:
        result = _dfs(child, descendants, colors)
        if result is True:
            return True
    colors[target] = Color.BLACK
    return False


def have_cycle(
        connections: list[EntitiesTypesConnection]
) -> bool:
    """Returns True if connections graph have cycle, else - False."""
    descendants = {}
    colors = {}
    for entity_type in EntityType:
        descendants[entity_type] = []
        colors[entity_type] = Color.WHITE

    for connection in connections:
        # Clear self-referenced types
        if connection.parent_type != connection.child_type:
            descendants[connection.parent_type].append(connection.child_type)

    # noinspection PyTypeChecker
    return _dfs(EntityType.COURSE, descendants, colors)
