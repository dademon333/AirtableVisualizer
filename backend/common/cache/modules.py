from aioredis import Redis

from courses.modules import get_all_courses_info, get_course_info
from .keys_formatters import get_course_key, get_all_courses_key, get_entities_types_connection_key
from .. import crud
from ..db import EntityType, session_factory
from ..redis import get_redis_cursor
from ..schemas.entities import CoursesSetInfo, CourseInfoExtended
from ..schemas.entities_types_connections import EntitiesTypesConnectionInfoExtended


async def get_course(
        course_id: int,
        redis_cursor: Redis
) -> CourseInfoExtended | None:
    course_data = await redis_cursor.get(get_course_key(course_id))

    if course_data is None:
        return None
    return CourseInfoExtended.parse_raw(course_data)


async def get_all_courses(
        redis_cursor: Redis,
        exclude_hidden: bool = False
) -> CoursesSetInfo | None:
    courses_data = await redis_cursor.get(get_all_courses_key(exclude_hidden))
    if courses_data is None:
        return None
    return CoursesSetInfo.parse_raw(courses_data)


async def get_entities_types_connection(
        connection_id: int,
        redis_cursor: Redis
) -> EntitiesTypesConnectionInfoExtended | None:
    result = await redis_cursor.get(get_entities_types_connection_key(connection_id))
    if result is None:
        return None
    return EntitiesTypesConnectionInfoExtended.parse_raw(result)


async def update_cache() -> None:
    db = session_factory()
    redis_cursor = await anext(get_redis_cursor())

    all_courses = await get_all_courses_info(db, exclude_hidden=False)
    await redis_cursor.set(
        get_all_courses_key(),
        all_courses.json(),
        ex=600
    )

    all_courses = await get_all_courses_info(db, exclude_hidden=True)
    await redis_cursor.set(
        get_all_courses_key(exclude_hidden=True),
        all_courses.json(),
        ex=600
    )

    all_courses = await crud.entities.get_by_type(db, EntityType.COURSE, limit=10000)
    for course in all_courses:
        course_data = await get_course_info(db, course.id)
        await redis_cursor.set(
            get_course_key(course.id),
            course_data.json(),
            ex=600
        )

    all_types_connections = await crud.entities_types_connections.get_all(db)
    for connection in all_types_connections:
        await redis_cursor.set(
            get_entities_types_connection_key(connection.id),
            EntitiesTypesConnectionInfoExtended.from_orm(connection).json(),
            ex=600
        )

    await db.close()


async def remove_course(
        course_id: int,
        redis_cursor: Redis
) -> None:
    await redis_cursor.delete(get_course_key(course_id))


async def remove_entities_types_connections(
        connection_id: int,
        redis_cursor: Redis
) -> None:
    await redis_cursor.delete(get_entities_types_connection_key(connection_id))
