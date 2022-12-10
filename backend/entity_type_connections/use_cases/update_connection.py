from entity_type_connections.dto import UpdateTypeConnectionInputDTO, \
    TypeConnectionOutputDTO, EntityTypeConnectionDBUpdateDTO
from entity_type_connections.exceptions import TypeConnectionNotFoundError
from entity_type_connections.repository import EntityTypeConnectionRepository


class UpdateTypeConnectionUseCase:
    def __init__(
            self,
            type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.type_connection_repository = type_connection_repository

    async def execute(
            self,
            connection_id: int,
            input_dto: UpdateTypeConnectionInputDTO,
    ) -> TypeConnectionOutputDTO:
        type_connection = await self.type_connection_repository.get_by_id(
            connection_id
        )
        if not type_connection:
            raise TypeConnectionNotFoundError()

        return await self.type_connection_repository.update(
            connection_id,
            EntityTypeConnectionDBUpdateDTO(
                **input_dto.dict(exclude_unset=True)
            )
        )
