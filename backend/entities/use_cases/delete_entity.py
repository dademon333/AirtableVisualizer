from typing import NoReturn

from entities.repository import EntityRepository


class DeleteEntityUseCase:
    def __init__(self, entity_repository: EntityRepository):
        self.repository = entity_repository

    async def execute(self, entity_id: int) -> NoReturn:
        await self.repository.delete(entity_id)
