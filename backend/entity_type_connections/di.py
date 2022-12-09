from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from entity_type_connections.repository import EntityTypeConnectionRepository
from entity_type_connections.use_cases.create_connection import \
    CreateTypeConnectionUseCase
from entity_type_connections.use_cases.delete_connection import \
    DeleteTypeConnectionUseCase
from entity_type_connections.use_cases.get_connection_info import \
    GetTypeConnectionUseCase
from entity_type_connections.use_cases.list_connections import \
    ListTypeConnectionsUseCase
from entity_type_connections.use_cases.update_connection import \
    UpdateTypeConnectionUseCase
from infrastructure.db import get_db


def get_entity_type_connection_repository(
        db: AsyncSession = Depends(get_db),
) -> EntityTypeConnectionRepository:
    return EntityTypeConnectionRepository(db)


def get_list_type_connections_use_case(
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        )
) -> ListTypeConnectionsUseCase:
    return ListTypeConnectionsUseCase(type_connection_repository)


def get_type_connection_use_case(
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        ),
) -> GetTypeConnectionUseCase:
    return GetTypeConnectionUseCase(
        type_connection_repository=type_connection_repository,
    )


def get_create_type_connection_use_case(
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        ),
) -> CreateTypeConnectionUseCase:
    return CreateTypeConnectionUseCase(type_connection_repository)


def get_update_type_connection_use_case(
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        ),
) -> UpdateTypeConnectionUseCase:
    return UpdateTypeConnectionUseCase(type_connection_repository)


def get_delete_type_connection_use_case(
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        ),
) -> DeleteTypeConnectionUseCase:
    return DeleteTypeConnectionUseCase(type_connection_repository)
