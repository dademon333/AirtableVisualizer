from entities.exceptions import EntityNotFoundError
from entities.repository import EntityRepository
from infrastructure.db import Entity


class GetEntityOrRaiseMixin:
    entity_repository: EntityRepository

    async def get_entity_or_raise(self, entity_id: int) -> Entity:
        entity = await self.entity_repository.get_by_id(entity_id)

        if not entity:
            raise EntityNotFoundError()

        return entity

