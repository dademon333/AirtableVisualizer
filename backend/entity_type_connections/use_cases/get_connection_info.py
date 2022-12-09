from entity_type_connections.dto import TypeConnectionExtendedOutputDTO
from entity_type_connections.exceptions import TypeConnectionNotFoundError
from entity_type_connections.repository import EntityTypeConnectionRepository


class GetTypeConnectionUseCase:
    def __init__(
            self,
            type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.type_connection_repository = type_connection_repository

    async def execute(
            self,
            connection_id: int
    ) -> TypeConnectionExtendedOutputDTO:
        type_connection = await self.type_connection_repository.\
            get_by_id_with_connections(connection_id)
        if not type_connection:
            raise TypeConnectionNotFoundError()

        return TypeConnectionExtendedOutputDTO.from_orm(type_connection)
