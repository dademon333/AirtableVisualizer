from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from courses.di import get_list_courses_use_case, \
    get_get_all_courses_info_use_case, get_course_info_use_case
from courses.dto import CourseOutputDTO, CourseWithConnectionsOutputDTO, \
    CoursesWithConnectionsOutputDTO
from courses.exceptions import NotACourseResponse, CourseNotFoundResponse
from courses.use_cases.get_all_courses_info import GetAllCoursesInfoUseCase
from courses.use_cases.get_course_info import GetCourseInfoUseCase
from courses.use_cases.list_courses import ListCoursesUseCase

courses_router = APIRouter()


@courses_router.get(
    '/list',
    response_model=list[CourseOutputDTO],
)
async def list_courses(
        use_case: ListCoursesUseCase = Depends(get_list_courses_use_case),
):
    """Возвращает список всех курсов."""
    return await use_case.execute()


@courses_router.get(
    '/all',
    response_model=CoursesWithConnectionsOutputDTO,
    response_class=ORJSONResponse,
)
async def get_all_courses(
        use_case: GetAllCoursesInfoUseCase = Depends(
            get_get_all_courses_info_use_case,
        ),
):
    """Возвращает полную информацию о всех курсах."""
    result = await use_case.execute()
    return ORJSONResponse(result.dict())


@courses_router.get(
    '/{course_id}',
    response_model=CourseWithConnectionsOutputDTO,
    response_class=ORJSONResponse,
    responses={
        400: {'model': NotACourseResponse},
        404: {'model': CourseNotFoundResponse}
    }
)
async def get_course_info(
        course_id: int,
        use_case: GetCourseInfoUseCase = Depends(get_course_info_use_case),
):
    """Возвращает информацию о курсе."""
    return await use_case.execute(course_id)
