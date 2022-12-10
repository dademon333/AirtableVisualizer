from courses.dto import CoursesWithConnectionsOutputDTO
from entities.repository import EntityRepository
from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import EntityType


class GetAllCoursesInfoUseCase:
    def __init__(
            self,
            entity_repository: EntityRepository,
            entity_connection_repository: EntityConnectionRepository,
    ):
        self.entity_repository = entity_repository
        self.entity_connection_repository = entity_connection_repository

    async def execute(self) -> CoursesWithConnectionsOutputDTO:
        entities = await self.entity_repository.get_all_connected()
        connections = await self.entity_connection_repository.get_all()
        courses = [x for x in entities if x.type == EntityType.COURSE]

        return CoursesWithConnectionsOutputDTO(
            courses=courses,
            entities=entities,
            entity_connections=connections,
        )
