from aioredis import Redis

from courses.modules import get_all_courses_info, get_course_info
from .. import crud
from ..db import EntityType, session_factory
from ..redis import get_redis_cursor
from ..schemas.entities import CoursesSetInfo, CourseInfo


async def get_course(
        course_id: int,
        redis_cursor: Redis
) -> CourseInfo | None:
    course_data = await redis_cursor.get(f'cache:course:{course_id}')

    if course_data is None:
        return None
    return CourseInfo.parse_raw(course_data)


async def get_all_courses(
        redis_cursor: Redis,
        exclude_hidden: bool = False
) -> CoursesSetInfo | None:
    if exclude_hidden:
        courses_data = await redis_cursor.get('cache:all_courses_without_hidden')
    else:
        courses_data = await redis_cursor.get('cache:all_courses')

    if courses_data is None:
        return None
    return CoursesSetInfo.parse_raw(courses_data)


async def update_cache() -> None:
    db = session_factory()
    redis_cursor = get_redis_cursor()

    all_courses = await get_all_courses_info(db, exclude_hidden=False)
    await redis_cursor.set('cache:all_courses', all_courses.json())

    all_courses = await get_all_courses_info(db, exclude_hidden=True)
    await redis_cursor.set('cache:all_courses_without_hidden', all_courses.json())

    all_courses = await crud.entities.get_by_type(db, EntityType.COURSE, limit=10000)
    for course in all_courses:
        course_data = await get_course_info(db, course.id)
        await redis_cursor.set(f'cache:course:{course.id}', course_data.json())

    await db.close()
