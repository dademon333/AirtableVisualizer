from typing import NoReturn

from entity_connections.exceptions import EntityConnectionNotFoundError
from entity_connections.repository import EntityConnectionRepository


class DisconnectEntitiesUseCase:
    def __init__(
            self,
            entity_connection_repository: EntityConnectionRepository,
    ):
        self.entity_connection_repository = entity_connection_repository

    async def execute(self, connection_id: int) -> NoReturn:
        connection = await self.entity_connection_repository.get_by_id(
            connection_id
        )

        if not connection:
            raise EntityConnectionNotFoundError()

        await self.entity_connection_repository.delete(connection.id)
