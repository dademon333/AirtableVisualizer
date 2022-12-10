from courses.dto import CourseOutputDTO
from entities.repository import EntityRepository
from infrastructure.db import EntityType


class ListCoursesUseCase:
    def __init__(
            self,
            entity_repository: EntityRepository,
    ):
        self.entity_repository = entity_repository

    async def execute(self) -> list[CourseOutputDTO]:
        courses = await self.entity_repository.get_by_type(
            entity_type=EntityType.COURSE,
            limit=10000
        )
        return [CourseOutputDTO.from_orm(x) for x in courses]
