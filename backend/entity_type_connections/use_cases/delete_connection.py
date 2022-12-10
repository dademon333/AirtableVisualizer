from typing import NoReturn

from entity_type_connections.exceptions import TypeConnectionNotFoundError
from entity_type_connections.repository import EntityTypeConnectionRepository


class DeleteTypeConnectionUseCase:
    def __init__(
            self,
            type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.type_connection_repository = type_connection_repository

    async def execute(self, connection_id: int) -> NoReturn:
        type_connection = await self.type_connection_repository.get_by_id(
            connection_id
        )
        if not type_connection:
            raise TypeConnectionNotFoundError()

        await self.type_connection_repository.delete(connection_id)
