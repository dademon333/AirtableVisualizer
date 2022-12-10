from entity_type_connections.dto import TypeConnectionOutputDTO
from entity_type_connections.repository import EntityTypeConnectionRepository


class ListTypeConnectionsUseCase:
    def __init__(
            self,
            entity_type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.entity_type_connection_repository = \
            entity_type_connection_repository

    async def execute(self) -> list[TypeConnectionOutputDTO]:
        result = await self.entity_type_connection_repository.get_many(
            limit=1000
        )
        return [TypeConnectionOutputDTO.from_orm(x) for x in result]
