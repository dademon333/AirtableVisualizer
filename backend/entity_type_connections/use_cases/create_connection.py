from enum import Enum

from entity_type_connections.dto import TypeConnectionOutputDTO, \
    CreateTypeConnectionInputDTO, EntityTypeConnectionDBInsertDTO
from entity_type_connections.exceptions import \
    TypeConnectionAlreadyExistsError, TypeConnectionCreatesCycleError
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import EntityTypeConnection, EntityType


class Color(str, Enum):
    WHITE = 'white'
    GREY = 'grey'
    BLACK = 'black'


class CreateTypeConnectionUseCase:
    def __init__(
            self,
            type_connection_repository: EntityTypeConnectionRepository,
    ):
        self.type_connection_repository = type_connection_repository

    async def execute(
            self,
            input_dto: CreateTypeConnectionInputDTO,
    ) -> TypeConnectionOutputDTO:
        all_connections = await self.type_connection_repository.get_all()

        if any(
            [
                x
                for x in all_connections
                if x.parent_type == input_dto.parent_type
                and x.child_type == input_dto.child_type
            ]
        ):
            raise TypeConnectionAlreadyExistsError()

        all_connections.append(
            EntityTypeConnection(
                parent_type=input_dto.parent_type,
                child_type=input_dto.child_type,
            )
        )
        if self.have_cycle(all_connections):
            raise TypeConnectionCreatesCycleError()

        result = await self.type_connection_repository.insert(
            EntityTypeConnectionDBInsertDTO(
                **input_dto.dict(exclude_unset=True)
            )
        )
        return TypeConnectionOutputDTO.from_orm(result)

    def have_cycle(self, connections: list[EntityTypeConnection]) -> bool:
        """Returns True if connections graph have cycle, else - False."""
        descendants = {}
        colors = {}
        for entity_type in EntityType:
            descendants[entity_type] = []
            colors[entity_type] = Color.WHITE

        for connection in connections:
            # Clear self-referenced types
            if connection.parent_type != connection.child_type:
                descendants[connection.parent_type].append(
                    connection.child_type
                )

        return self.dfs(EntityType.COURSE, descendants, colors)  # noqa

    def dfs(
            self,
            target: EntityType,
            descendants: dict[EntityType, list[EntityType]],
            colors: dict[EntityType, Color]
    ) -> bool:
        if colors[target] == Color.BLACK:
            return False
        if colors[target] == Color.GREY:
            return True

        colors[target] = Color.GREY
        for child in descendants[target]:
            result = self.dfs(child, descendants, colors)
            if result is True:
                return True

        colors[target] = Color.BLACK
        return False
