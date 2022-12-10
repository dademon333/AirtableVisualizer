from fastapi import Depends

from courses.use_cases.get_all_courses_info import GetAllCoursesInfoUseCase
from courses.use_cases.get_course_info import GetCourseInfoUseCase
from courses.use_cases.list_courses import ListCoursesUseCase
from entities.di import get_entity_repository
from entities.repository import EntityRepository
from entity_connections.di import get_entity_connection_repository
from entity_connections.repository import EntityConnectionRepository


def get_list_courses_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
) -> ListCoursesUseCase:
    return ListCoursesUseCase(entity_repository)


def get_get_all_courses_info_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
        entity_connection_repository: EntityConnectionRepository = Depends(
            get_entity_connection_repository
        )
) -> GetAllCoursesInfoUseCase:
    return GetAllCoursesInfoUseCase(
        entity_repository,
        entity_connection_repository,
    )


def get_course_info_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
        entity_connection_repository: EntityConnectionRepository = Depends(
            get_entity_connection_repository
        ),
) -> GetCourseInfoUseCase:
    return GetCourseInfoUseCase(
        entity_repository,
        entity_connection_repository,
    )
