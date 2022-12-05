from entities.dto import EntityOutputDTO
from entities.repository import EntityRepository


class GetEntityUseCase:
    def __init__(self, entity_repository: EntityRepository):
        self.repository = entity_repository

    async def execute(self, entity_id: int) -> EntityOutputDTO | None:
        return await self.repository.get_by_id(entity_id)
