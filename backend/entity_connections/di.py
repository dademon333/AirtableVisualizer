from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from entities.di import get_entity_repository
from entities.repository import EntityRepository
from entity_connections.repository import EntityConnectionRepository
from entity_connections.use_cases.connect_entities import \
    ConnectEntitiesUseCase
from entity_connections.use_cases.disconnect_entities import \
    DisconnectEntitiesUseCase
from entity_type_connections.di import get_entity_type_connection_repository
from entity_type_connections.repository import EntityTypeConnectionRepository
from infrastructure.db import get_db


def get_entity_connection_repository(
        db: AsyncSession = Depends(get_db),
) -> EntityConnectionRepository:
    return EntityConnectionRepository(db)


def get_connect_entities_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
        entity_connection_repository: EntityConnectionRepository = Depends(
            get_entity_connection_repository
        ),
        type_connection_repository: EntityTypeConnectionRepository = Depends(
            get_entity_type_connection_repository
        ),
) -> ConnectEntitiesUseCase:
    return ConnectEntitiesUseCase(
        entity_repository,
        entity_connection_repository,
        type_connection_repository
    )


def get_disconnect_entities_use_case(
        entity_connection_repository: EntityConnectionRepository = Depends(
            get_entity_connection_repository
        ),
) -> DisconnectEntitiesUseCase:
    return DisconnectEntitiesUseCase(entity_connection_repository)