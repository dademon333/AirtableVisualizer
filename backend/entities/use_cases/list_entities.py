
from entities.dto import EntityOutputDTO
from entities.repository import EntityRepository
from infrastructure.db import EntityType


class ListEntitiesUseCase:
    def __init__(self, entity_repository: EntityRepository):
        self.repository = entity_repository

    async def execute(
            self,
            entity_type: EntityType,
            limit: int = 250,
            offset: int = 0
    ) -> list[EntityOutputDTO]:
        entities = await self.repository.list_by_type(
            entity_type, limit, offset
        )
        return [EntityOutputDTO.from_orm(x) for x in entities]
