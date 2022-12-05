from entities.dto import EntityOutputDTO
from entities.repository import EntityRepository
from infrastructure.db import EntityType


class SearchEntitiesUseCase:
    def __init__(self, entity_repository: EntityRepository):
        self.repository = entity_repository

    async def execute(
            self,
            query: str,
            entity_type: EntityType | None = None,
            limit: int = 250,
            offset: int = 0,
    ) -> list[EntityOutputDTO]:
        entities = await self.repository.search_by_name(
            query, entity_type, limit, offset
        )
        return [EntityOutputDTO.from_orm(x) for x in entities]
