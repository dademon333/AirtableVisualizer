from entities.exceptions import EntityNotFoundError
from entities.repository import EntityRepository
from entity_connections.dto import EntityConnectionInputDTO, \
    EntityConnectionDBInsertDTO
from entity_connections.exceptions import EntityConnectionAlreadyExistsError
from entity_connections.repository import EntityConnectionRepository
from entity_type_connections.exceptions import TypeConnectionNotFoundError
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import EntityConnection


class ConnectEntitiesUseCase:
    def __init__(
            self,
            entity_repository: EntityRepository,
            entity_connection_repository: EntityConnectionRepository,
            entity_type_connection_repository: EntityTypeConnectionRepository
    ):
        self.entity_repository = entity_repository
        self.entity_connection_repository = entity_connection_repository
        self.entity_type_connection_repository = \
            entity_type_connection_repository

    async def execute(
            self,
            input_dto: EntityConnectionInputDTO,
    ) -> EntityConnection:
        parent_entity = await self.entity_repository.get_by_id(
            input_dto.parent_id
        )
        child_entity = await self.entity_repository.get_by_id(
            input_dto.child_id
        )
        if not parent_entity or not child_entity:
            raise EntityNotFoundError()

        type_connection = await self.entity_type_connection_repository.\
            get_by_types(
                parent_type=parent_entity.type,
                child_type=child_entity.type,
            )
        if not type_connection:
            raise TypeConnectionNotFoundError()

        is_exists = await self.entity_connection_repository.get_by_entities(
            parent_id=parent_entity.id,
            child_id=child_entity.id,
        )
        if is_exists:
            raise EntityConnectionAlreadyExistsError()

        return await self.entity_connection_repository.insert(
            EntityConnectionDBInsertDTO(
                parent_id=parent_entity.id,
                child_id=child_entity.id,
                type_connection_id=type_connection.id
            )
        )
