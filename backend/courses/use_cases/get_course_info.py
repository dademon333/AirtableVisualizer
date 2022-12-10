from typing import NoReturn

from courses.dto import CourseWithConnectionsOutputDTO
from courses.exceptions import CourseNotFoundError, NotACourseError
from entities.repository import EntityRepository
from entity_connections.repository import EntityConnectionRepository
from infrastructure.db import EntityType, Entity, EntityConnection


class GetCourseInfoUseCase:
    def __init__(
            self,
            entity_repository: EntityRepository,
            entity_connection_repository: EntityConnectionRepository,
    ):
        self.entity_repository = entity_repository
        self.connection_repository = entity_connection_repository

    async def execute(self, course_id: int) -> CourseWithConnectionsOutputDTO:
        course = await self.entity_repository.get_by_id(course_id)

        if not course:
            raise CourseNotFoundError()

        if course.type != EntityType.COURSE:
            raise NotACourseError()

        all_entities = [course]
        all_connections = []
        await self.load_children(
            entities=[course],
            all_entities=all_entities,
            all_connections=all_connections,
        )

        entities, connections = self.filter_doubles(
            all_entities=all_entities,
            all_connections=all_connections,
        )
        return CourseWithConnectionsOutputDTO(
            id=course.id,
            name=course.name,
            description=course.description,
            entities=entities,
            entity_connections=connections,
        )

    async def load_children(
            self,
            entities: list[Entity],
            all_entities: list[Entity],
            all_connections: list[EntityConnection],
    ) -> NoReturn:
        child_connects = await self.connection_repository.get_by_parent_ids(
            [x.id for x in entities]
        )

        if not child_connects:
            return

        child_entities = await self.entity_repository.get_by_ids(
            [x.child_id for x in child_connects]
        )

        all_entities.extend(child_entities)
        all_connections.extend(child_connects)
        await self.load_children(
            entities=child_entities,
            all_entities=all_entities,
            all_connections=all_connections,
        )

    @staticmethod
    def filter_doubles(
            all_entities: list[Entity],
            all_connections: list[EntityConnection],
    ) -> tuple[list[Entity], list[EntityConnection]]:
        entity_ids = set()
        connection_ids = set()
        result_entities = []
        result_connections = []

        for entity in all_entities:
            if entity.id not in entity_ids:
                result_entities.append(entity)

        for connection in all_connections:
            if connection.id not in connection_ids:
                result_connections.append(connection)

        return result_entities, result_connections
