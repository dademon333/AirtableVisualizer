import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.responses import OkResponse, EditorStatusRequiredResponse, UnauthorizedResponse
from common.security.auth import UserStatusChecker, get_user_id, get_user_status, can_access
from common.db import get_db, UserStatus, EntityType, ChangedTable
from common.schemas.entities import EntityInfo, CourseInfo, CoursesSetInfo
from common.schemas.hidden_courses import HiddenCourseCreate
from .modules import get_course_info, get_all_courses_info
from .schemas import CourseNotFoundResponse, NotACourseErrorResponse

courses_router = APIRouter()


@courses_router.get(
    '/list',
    response_model=list[EntityInfo]
)
async def list_courses(
        user_status: UserStatus | None = Depends(get_user_status),
        db: AsyncSession = Depends(get_db),
):
    """Возвращает список всех доступных для пользователя курсов."""
    courses = await crud.entities.get_by_type(db, EntityType.COURSE, limit=10000)
    courses = [EntityInfo.from_orm(x) for x in courses]
    if not can_access(user_status, min_status=UserStatus.EDITOR):
        hidden_courses = await crud.hidden_courses.get_all(db)
        courses = [x for x in courses if x.id not in hidden_courses]
    return courses


@courses_router.get(
    '/info/all',
    response_model=CoursesSetInfo,
    response_class=ORJSONResponse
)
async def get_all_courses_info_(
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о всех доступных для пользователя курсах."""
    if can_access(user_status, min_status=UserStatus.EDITOR):
        result = await get_all_courses_info(db)
    else:
        result = await get_all_courses_info(db, exclude_hidden=True)

    return ORJSONResponse(result.dict())


@courses_router.get(
    '/info/{course_id}',
    response_model=CourseInfo,
    response_class=ORJSONResponse,
    responses={
        400: {'model': NotACourseErrorResponse},
        404: {'model': CourseNotFoundResponse}
    }
)
async def get_course_info_(
        course_id: int,
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
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
    return OkResponse()
