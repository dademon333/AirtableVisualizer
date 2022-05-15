import asyncio

import sqlalchemy.exc
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud, cache
from common.redis import get_redis_cursor
from common.responses import OkResponse, EditorStatusRequiredResponse, UnauthorizedResponse
from common.security.auth import UserStatusChecker, get_user_id, get_user_status, can_access
from common.db import get_db, UserStatus, EntityType, ChangedTable
from common.schemas.entities import EntityInfo, CourseInfoExtended, CoursesSetInfo, CourseInfo
from common.schemas.hidden_courses import HiddenCourseCreate
from common.sqlalchemy_modules import convert_instance_to_dict
from .modules import get_course_info, get_all_courses_info
from .schemas import CourseNotFoundResponse, NotACourseErrorResponse

courses_router = APIRouter()


@courses_router.get(
    '/list',
    response_model=list[CourseInfo]
)
async def list_courses(
        user_status: UserStatus | None = Depends(get_user_status),
        db: AsyncSession = Depends(get_db),
):
    """Возвращает список всех доступных для пользователя курсов."""
    courses = await crud.entities.get_by_type(db, EntityType.COURSE, limit=10000)
    hidden_courses = await crud.hidden_courses.get_all(db)
    if not can_access(user_status, min_status=UserStatus.EDITOR):
        courses = [x for x in courses if x.id not in hidden_courses]

    courses = [
        CourseInfo(
            **convert_instance_to_dict(x),
            is_hidden=x.id in hidden_courses
        )
        for x in courses
    ]
    return courses


@courses_router.get(
    '/info/all',
    response_model=CoursesSetInfo,
    response_class=ORJSONResponse
)
async def get_all_courses_info_(
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Возвращает информацию о всех доступных для пользователя курсах."""
    if can_access(user_status, min_status=UserStatus.EDITOR):
        exclude_hidden = False
    else:
        exclude_hidden = True

    if (result := await cache.get_all_courses(redis_cursor, exclude_hidden)) is None:
        result = await get_all_courses_info(db, exclude_hidden=exclude_hidden)

    return ORJSONResponse(result.dict())


@courses_router.get(
    '/info/{course_id}',
    response_model=CourseInfoExtended,
    response_class=ORJSONResponse,
    responses={
        400: {'model': NotACourseErrorResponse},
        404: {'model': CourseNotFoundResponse}
    }
)
async def get_course_info_(
        course_id: int,
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Возвращает информацию о курсе."""
    course = await crud.entities.get_by_id(db, course_id)
    hidden_courses = await crud.hidden_courses.get_all(db)

    if course is None \
            or course.id in hidden_courses \
            and not can_access(user_status, min_status=UserStatus.EDITOR):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CourseNotFoundResponse().detail
        )
    if course.type != EntityType.COURSE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotACourseErrorResponse().detail
        )

    if (result := await cache.get_course(course_id, redis_cursor)) is None:
        result = await get_course_info(db, course_id)

    return ORJSONResponse(result.dict())


@courses_router.post(
    '/hide/{course_id}',
    response_model=OkResponse,
    responses={
        400: {'model': NotACourseErrorResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': CourseNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def hide_course(
        course_id: int,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Скрывает курс от обычных пользователей. Требует статус editor."""
    course = await crud.entities.get_by_id(db, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CourseNotFoundResponse().detail
        )
    if course.type != EntityType.COURSE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotACourseErrorResponse().detail
        )

    try:
        hidden_course = await crud.hidden_courses.create(
            db,
            HiddenCourseCreate(course_id=course_id)
        )
    except sqlalchemy.exc.IntegrityError:
        pass
    else:
        await crud.change_log.log_create_operation(
            db=db,
            editor_id=editor_id,
            table=ChangedTable.HIDDEN_COURSES,
            element_id=hidden_course.id
        )
        asyncio.create_task(cache.update_cache())

    return OkResponse()


@courses_router.delete(
    '/unhide/{course_id}',
    response_model=OkResponse,
    responses={
        400: {'model': NotACourseErrorResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': CourseNotFoundResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def unhide_course(
        course_id: int,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Убирает курс из списка скрытых. Требует статус editor."""
    course = await crud.entities.get_by_id(db, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CourseNotFoundResponse().detail
        )
    if course.type != EntityType.COURSE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotACourseErrorResponse().detail
        )

    hidden_course = await crud.hidden_courses.get_by_course_id(db, course_id)
    if hidden_course is not None:
        await crud.hidden_courses.delete_by_course_id(db, course_id)
        await crud.change_log.log_delete_operation(
            db,
            editor_id=editor_id,
            table=ChangedTable.HIDDEN_COURSES,
            element_instance=hidden_course
        )
        asyncio.create_task(cache.update_cache())
    return OkResponse()
