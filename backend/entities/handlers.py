import asyncio

from aioredis import Redis
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud, cache
from common.db import UserStatus, EntityType, get_db, ChangedTable
from common.redis import get_redis_cursor
from common.responses import EditorStatusRequiredResponse, UnauthorizedResponse, OkResponse
from common.schemas.entities import EntityInfo, EntityCreate, EntityUpdate
from common.security.auth import UserStatusChecker, get_user_id
from .schemas import EntityNotFoundResponse

entities_router = APIRouter()


@entities_router.get(
    '/list/{entity_type}',
    response_model=list[EntityInfo],
    response_class=ORJSONResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def list_entities(
        entity_type: EntityType,
        db: AsyncSession = Depends(get_db),
        limit: int = Query(250, le=1000),
        offset: int = 0
):
    """Возвращает список сущностей по их типу. Требует статус editor."""
    entities = await crud.entities.get_by_type(db, entity_type, limit, offset)
    return ORJSONResponse([EntityInfo.from_orm(x).dict() for x in entities])


@entities_router.get(
    '/search/{entity_type}',
    response_model=list[EntityInfo],
    response_class=ORJSONResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def search_entity(
        entity_type: EntityType,
        db: AsyncSession = Depends(get_db),
        query: str = Query(...),
        limit: int = Query(250, le=1000),
        offset: int = 0
):
    """Ищет сущности по названию и типу. case-insensitive. Требует статус editor."""
    entities = await crud.entities.search_by_name(db, entity_type, query, limit, offset)
    return ORJSONResponse([EntityInfo.from_orm(x).dict() for x in entities])


@entities_router.post(
    '/create',
    response_model=EntityInfo,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse}
    }
)
async def create_entity(
        create_form: EntityCreate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает новую сущность. Требует статус editor."""
    entity = await crud.entities.create(db, create_form)

    await crud.change_log.log_create_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES,
        element_id=entity.id
    )
    asyncio.create_task(cache.update_cache())
    return EntityInfo.from_orm(entity)


@entities_router.put(
    '/update/{entity_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntityNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def update_entity(
        entity_id: int,
        update_form: EntityUpdate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о сущности.

    Все поля в теле запроса являются необязательными,
    передавать нужно только необходимые дня обновления.
    Требует статус editor.

    """
    entity = await crud.entities.get_by_id(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntityNotFoundResponse().detail
        )

    old_instance = dict(entity.__dict__)
    await crud.entities.update(db, entity_id, update_form)

    await crud.change_log.log_update_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES,
        update_form=update_form,
        old_instance=old_instance,
        new_instance=entity
    )
    asyncio.create_task(cache.update_cache())
    return OkResponse()


@entities_router.delete(
    '/delete/{entity_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntityNotFoundResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def delete_entity(
        entity_id: int,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Удаляет сущность. Требует статус editor."""
    entity = await crud.entities.get_by_id(db, entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntityNotFoundResponse().detail
        )

    if entity.type == EntityType.COURSE:
        await cache.remove_course(entity_id, redis_cursor)

    delete_log = await crud.change_log.log_delete_operation(
        db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES,
        element_instance=entity
    )

    adjacent_connections = await crud.entities_connections.get_by_entity_id(db, entity_id)
    for entities_connection in adjacent_connections:
        await crud.change_log.log_delete_operation(
            db,
            editor_id=editor_id,
            table=ChangedTable.ENTITIES_CONNECTIONS,
            element_instance=entities_connection,
            parent_change_id=delete_log.id
        )

    await crud.entities.delete(db, entity_id)
    asyncio.create_task(cache.update_cache())
    return OkResponse()
