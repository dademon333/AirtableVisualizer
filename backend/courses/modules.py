from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import EntityType, EntitiesTypesConnection, EntitiesConnection, Entity
from common.schemas.entities import CourseInfoExtended, EntityInfo, CoursesSetInfo, EntityInfoReduced
from common.schemas.entities_connections import EntitiesConnectionInfoReduced
from common.schemas.entities_types_connections import EntitiesTypesConnectionInfoExtended


def connectivity_component_dfs(
        target: EntityType,
        connections: dict[EntityType, list[EntityType]],
        is_used: dict[EntityType, bool]
) -> None:
    if is_used[target]:
        return

    is_used[target] = True
    for adjacent in connections[target]:
        connectivity_component_dfs(adjacent, connections, is_used)


def get_connectivity_component(
        types_connections: list[EntitiesTypesConnection]
) -> list[EntityType]:
    """Returns entity types in one graph connectivity component with course."""
    is_used = {x: False for x in EntityType}
    connections = {x: [] for x in EntityType}
    for connection in types_connections:
        connections[connection.parent_type].append(connection.child_type)
        connections[connection.child_type].append(connection.parent_type)

    connectivity_component_dfs(EntityType.COURSE, connections, is_used)
    return [key for key in is_used if is_used[key]]


def remove_external_connections(
        types_connections: list[EntitiesTypesConnection]
) -> list[EntitiesTypesConnection]:
    """Filter types connections which are not in the same connectivity component with course."""
    entities = get_connectivity_component(types_connections)
    return [
        x
        for x in types_connections
        if x.parent_type in entities or x.child_type in entities
    ]


def get_dependent_branches_heads(
        types_connections: list[EntitiesTypesConnection]
) -> list[EntityType]:
    """Returns heads of dependent branches.

    Depends branch - branch of tree which have own head (not course entity type)
    and loads on the basis of main branch (where head is course).
    Head - entity type without parents.

    """
    heads = list({x.parent_type for x in types_connections})
    for connection in types_connections:
        if connection.child_type in heads:
            heads.remove(connection.child_type)

    if EntityType.COURSE in heads:
        heads.remove(EntityType.COURSE)

    return heads


def get_dependent_branch_types(
        head: EntityType,
        types_connections: list[EntitiesTypesConnection]
) -> list[EntityType]:
    """Returns all entities types in dependent branch."""
    types = [head]

    while True:
        next_type = [
            x.child_type
            for x in types_connections
            if x.child_type not in types
            and all(
                y.parent_type in types
                for y in types_connections
                if y.child_type == x.child_type
            )
        ]
        if next_type == []:
            break
        types.append(next_type[0])

    return types


def get_dependent_branches(
        types_connections: list[EntitiesTypesConnection]
) -> list[list[EntityType]]:
    branches_heads = get_dependent_branches_heads(types_connections)
    return [get_dependent_branch_types(x, types_connections) for x in branches_heads]


async def fill_self_connected_entities(
        db: AsyncSession,
        adjacent_connections: list[EntitiesTypesConnection],
        entities: dict[EntityType, set[Entity]],
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]]
) -> None:
    self_connection = [
        x
        for x in adjacent_connections
        if x.parent_type == x.child_type
    ]
    if self_connection == []:
        return
    connection = self_connection[0]
    entity_type = connection.child_type

    while True:
        parent_entities = [x.id for x in entities[entity_type]]
        new_connections = [
            x
            for x in connection.entities_connections
            if x.parent_id in parent_entities
        ]
        new_connections = set(new_connections) - set(entities_connections.get(connection, []))
        if new_connections == set():
            return

        entities_connections[connection].extend(list(new_connections))
        entities[entity_type].update(
            await crud.entities.get_by_ids(
                db,
                list(set(x.child_id for x in new_connections))
            )
        )


async def fill_main_branch(
        db: AsyncSession,
        types_connections: list[EntitiesTypesConnection],
        entities: dict[EntityType, set[Entity]],
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]],
        all_branches_types: list[EntityType]
) -> None:
    while True:
        next_type = [
            x.child_type
            for x in types_connections
            if x.child_type not in entities
            and all(
                y.parent_type in entities
                for y in types_connections
                if y.child_type == x.child_type
                and y.child_type != y.parent_type
                and y.parent_type not in all_branches_types
            )
        ]
        if next_type == []:
            break

        next_type = next_type[0]
        entities[next_type] = set()
        adjacent_connections = [
            x
            for x in types_connections
            if x.child_type == next_type
            and x.parent_type not in all_branches_types
        ]

        for connection in adjacent_connections:
            parent_entities = [x.id for x in entities[connection.parent_type]]
            new_connections = [
                x
                for x in connection.entities_connections
                if x.parent_id in parent_entities
            ]
            if new_connections == []:
                continue

            entities_connections[connection] = new_connections
            entities[next_type].update(
                await crud.entities.get_by_ids(
                    db,
                    list(set(x.child_id for x in new_connections))
                )
            )

        await fill_self_connected_entities(
            db,
            adjacent_connections,
            entities,
            entities_connections
        )


async def fill_branch_in_reverse_mode(
        db: AsyncSession,
        branch_nodes: list[EntityType],
        types_connections: list[EntitiesTypesConnection],
        entities: dict[EntityType, set[Entity]],
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]]
) -> None:
    while True:
        next_type = [
            x.parent_type
            for x in types_connections
            if x.parent_type not in entities
            and x.parent_type in branch_nodes
            and all(
                y.child_type in entities
                for y in types_connections
                if y.parent_type == x.parent_type
                and y.parent_type != y.child_type
            )
        ]
        if next_type == []:
            break

        next_type = next_type[0]
        entities[next_type] = set()
        adjacent_connections = [
            x
            for x in types_connections
            if x.parent_type == next_type
        ]
        for connection in adjacent_connections:
            child_entities = [x.id for x in entities[connection.child_type]]
            new_connections = [
                x
                for x in connection.entities_connections
                if x.child_id in child_entities
            ]
            if new_connections == []:
                continue

            entities_connections[connection] = new_connections
            entities[next_type].update(
                await crud.entities.get_by_ids(
                    db,
                    list(set(x.parent_id for x in new_connections))
                )
            )

        await fill_self_connected_entities(
            db,
            adjacent_connections,
            entities,
            entities_connections
        )


async def fill_branch_in_default_mode(
        db: AsyncSession,
        branch_nodes: list[EntityType],
        types_connections: list[EntitiesTypesConnection],
        entities: dict[EntityType, set[Entity]],
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]]
) -> None:
    while True:
        next_type = [
            x.child_type
            for x in types_connections
            if x.child_type not in entities
            and x.child_type in branch_nodes
            and all(
                y.parent_type in entities
                for y in types_connections
                if y.child_type == x.child_type
                and y.child_type != y.parent_type
            )
        ]
        if next_type == []:
            break

        next_type = next_type[0]
        entities[next_type] = set()
        adjacent_connections = [
            x
            for x in types_connections
            if x.child_type == next_type
        ]
        for connection in adjacent_connections:
            parent_entities = [x.id for x in entities[connection.parent_type]]
            new_connections = [
                x
                for x in connection.entities_connections
                if x.parent_id in parent_entities
            ]
            if new_connections == []:
                continue

            entities_connections[connection] = new_connections
            entities[next_type].update(
                await crud.entities.get_by_ids(
                    db,
                    list(set(x.child_id for x in new_connections))
                )
            )

        await fill_self_connected_entities(
            db,
            adjacent_connections,
            entities,
            entities_connections
        )


async def fill_branch(
        db: AsyncSession,
        branch_nodes: list[EntityType],
        types_connections: list[EntitiesTypesConnection],
        entities: dict[EntityType, set[Entity]],
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]]
) -> None:
    await fill_branch_in_reverse_mode(
        db,
        branch_nodes,
        types_connections,
        entities,
        entities_connections
    )
    await fill_branch_in_default_mode(
        db,
        branch_nodes,
        types_connections,
        entities,
        entities_connections
    )


def prepare_result(
        entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]],
        entities: dict[EntityType, set[Entity]]
) -> CoursesSetInfo:
    all_entities = set()
    for batch in entities.values():
        all_entities.update(batch)
    all_entities = [EntityInfo.from_orm(x) for x in all_entities]

    connections = [
        EntitiesTypesConnectionInfoExtended(
            id=types_conn.id,
            parent_type=types_conn.parent_type,
            child_type=types_conn.child_type,
            entities_connections=[
                EntitiesConnectionInfoReduced.from_orm(x)
                for x in set(entities_conn)
            ]
        )
        for types_conn, entities_conn in entities_connections.items()
    ]

    return CoursesSetInfo(
        connections=connections,
        entities={str(x.id): EntityInfoReduced.from_orm(x) for x in all_entities}
    )


async def get_courses_info(
        db: AsyncSession,
        course_ids: list[int]
) -> CoursesSetInfo:
    entities = {
        EntityType.COURSE: await crud.entities.get_by_ids(db, course_ids)
    }
    entities_connections: dict[EntitiesTypesConnection, list[EntitiesConnection]] = {}
    types_connections = await crud.entities_types_connections.get_all(db)
    types_connections = remove_external_connections(types_connections)

    branches = get_dependent_branches(types_connections)
    all_branches_types = sum(branches, [])

    await fill_main_branch(
        db,
        types_connections,
        entities,
        entities_connections,
        all_branches_types
    )
    for branch_nodes in branches:
        await fill_branch(
            db,
            branch_nodes,
            types_connections,
            entities,
            entities_connections
        )

    return prepare_result(entities_connections, entities)


async def get_course_info(
        db: AsyncSession,
        course_id: int
) -> CourseInfoExtended:
    course = await crud.entities.get_by_id(db, course_id)
    course_info = await get_courses_info(db, [course_id])
    is_hidden = await crud.hidden_courses.is_hidden(db, course_id)

    return CourseInfoExtended(
        name=course.name,
        type=course.type,
        size=course.size,
        description=course.description,
        study_time=course.study_time,
        id=course.id,
        is_hidden=is_hidden,
        connections=course_info.connections,
        entities=course_info.entities
    )


async def get_all_courses_info(
        db: AsyncSession,
        exclude_hidden: bool = False
) -> CoursesSetInfo:
    courses = await crud.entities.get_by_type(db, EntityType.COURSE, limit=10000)
    courses = [x.id for x in courses]

    if exclude_hidden:
        hidden_courses = await crud.hidden_courses.get_all(db)
        courses = [x for x in courses if x not in hidden_courses]

    return await get_courses_info(db, courses)
