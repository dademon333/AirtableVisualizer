from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from entities.repository import EntityRepository
from entities.use_cases.create_entity import CreateEntityUseCase
from entities.use_cases.delete_entity import DeleteEntityUseCase
from entities.use_cases.get_entity import GetEntityUseCase
from entities.use_cases.list_entities import ListEntitiesUseCase
from entities.use_cases.search_entity import SearchEntitiesUseCase
from entities.use_cases.update_entity import UpdateEntityUseCase
from infrastructure.db import get_db


def get_entity_repository(
        db: AsyncSession = Depends(get_db)
) -> EntityRepository:
    return EntityRepository(db)


def get_get_entity_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository)
) -> GetEntityUseCase:
    return GetEntityUseCase(entity_repository)


def get_list_entities_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository)
) -> ListEntitiesUseCase:
    return ListEntitiesUseCase(entity_repository)


def get_search_entities_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository)
) -> SearchEntitiesUseCase:
    return SearchEntitiesUseCase(entity_repository)


def get_create_entity_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
) -> CreateEntityUseCase:
    return CreateEntityUseCase(entity_repository)


def get_update_entity_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
) -> UpdateEntityUseCase:
    return UpdateEntityUseCase(entity_repository)


def get_delete_entity_use_case(
        entity_repository: EntityRepository = Depends(get_entity_repository),
) -> DeleteEntityUseCase:
    return DeleteEntityUseCase(entity_repository)
