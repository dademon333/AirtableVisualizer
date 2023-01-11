from entity_type_connections.dto import TypeConnectionExtendedOutputDTO
from entity_type_connections.repository import EntityTypeConnectionRepository


class GetAllConnectionsUseCase:
    def __init__(
            self,
            type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.type_connection_repository = type_connection_repository

    async def execute(self) -> dict[int, TypeConnectionExtendedOutputDTO]:
        return await self.type_connection_repository.get_all_with_connections()
