from entities.dto import EntityOutputDTO, EntityDBUpdateDTO, \
    UpdateEntityInputDTO
from entities.repository import EntityRepository
from entities.use_cases.get_entity_or_raise_mixin import GetEntityOrRaiseMixin


class UpdateEntityUseCase(GetEntityOrRaiseMixin):
    def __init__(self, entity_repository: EntityRepository):
        self.entity_repository = entity_repository

    async def execute(
            self,
            entity_id: int,
            update_dto: UpdateEntityInputDTO,
    ) -> EntityOutputDTO:
        entity = await self.get_entity_or_raise(entity_id)
        await self.entity_repository.update(
            entity_id,
            EntityDBUpdateDTO(**update_dto.dict(exclude_unset=True))
        )
        return entity
