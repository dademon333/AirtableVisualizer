import time

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis

from api.modules import get_all_courses, get_entire_course
from api.schemas import AllCourses, EntireCourse
from utils.psql_utils import get_psql_cursor
from utils.redis_utils import get_redis_cursor

api_router = APIRouter()


@api_router.get('/courses/all', response_model=AllCourses)
async def get_all_courses_view(
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    if (all_courses := redis_cursor.get('cache:all_courses')) is not None:
        all_courses = AllCourses.parse_raw(all_courses)
    else:
        all_courses = get_all_courses(get_psql_cursor())

    return all_courses


@api_router.get('/courses/{course_id}', response_model=EntireCourse)
async def get_entire_course_view(
        course_id: str,
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    if (course := redis_cursor.get(f'cache:courses:{course_id}')) is not None:
        course = EntireCourse.parse_raw(course)
    else:
        course = get_entire_course(course_id, get_psql_cursor())

    if course is None:
        raise HTTPException(
            status_code=404,
            detail='Course not found'
        )
    return course
