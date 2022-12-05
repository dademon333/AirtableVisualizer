from entities.dto import CreateEntityInputDTO, EntityDBInsertDTO
from entities.repository import EntityRepository
from infrastructure.db import Entity


class CreateEntityUseCase:
    def __init__(self, entity_repository: EntityRepository):
        self.entity_repository = entity_repository

    async def execute(self, input_dto: CreateEntityInputDTO) -> Entity:
        entity = await self.entity_repository.insert(
            EntityDBInsertDTO(**input_dto.dict(exclude_unset=True))
        )
        return entity
