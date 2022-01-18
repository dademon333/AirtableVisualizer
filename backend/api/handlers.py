import json

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import ORJSONResponse
from redis import Redis

from api.modules import get_all_courses, get_entire_course
from api.schemas import AllCourses, EntireCourse
from utils.psql_utils import get_psql_cursor
from utils.redis_utils import get_redis_cursor

api_router = APIRouter()


@api_router.get('/course/all', response_model=AllCourses, response_class=ORJSONResponse)
async def get_all_courses_view(
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Возвращает информацию о всех курсах, темах, знаниях, квантах и компетенциях.
    Предполагается, что при входе на главную страницу пользователю будут отображаться данные отсюда
    """
    if (all_courses := redis_cursor.get('cache:all_courses')) is not None:
        all_courses = json.loads(all_courses)
    else:
        all_courses = get_all_courses(get_psql_cursor())

    return ORJSONResponse(all_courses)


@api_router.get('/course/{course_id}', response_model=EntireCourse, response_class=ORJSONResponse)
async def get_entire_course_view(
        course_id: str = Path(..., description="Идентификатор курса"),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Возвращает полную информацию о конкретном курсе вплоть до профессий и компетенций СУОС"""
    if (course := redis_cursor.get(f'cache:courses:{course_id}')) is not None:
        course = json.loads(course)
    else:
        course = get_entire_course(course_id, get_psql_cursor())

    if course is None:
        raise HTTPException(
            status_code=404,
            detail='Course not found'
        )
    return ORJSONResponse(course)
