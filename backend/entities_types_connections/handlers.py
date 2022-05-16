import asyncio

import sqlalchemy.exc
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud, cache
from common.redis import get_redis_cursor
from common.responses import OkResponse, UnauthorizedResponse, AdminStatusRequiredResponse, EditorStatusRequiredResponse
from common.security.auth import UserStatusChecker, get_user_id
from common.db import UserStatus, get_db, ChangedTable, EntitiesTypesConnection
from entities_types_connections.modules import have_cycle
from entities_types_connections.schemas import ConnectionNotFoundResponse, \
    ConnectionAlreadyExistsResponse, ConnectionCreatesCycleErrorResponse
from common.schemas.entities_types_connections import EntitiesTypesConnectionUpdate, \
    EntitiesTypesConnectionCreate, EntitiesTypesConnectionInfo, EntitiesTypesConnectionInfoExtended

types_connections_router = APIRouter()


@types_connections_router.get(
    '/list',
    response_model=list[EntitiesTypesConnectionInfo]
)
async def list_connections(
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о связях между типами сущностей.

    На основе этой информации необходимо строить колонки связей в таблицах.
    Если в названии колонки указан null, её отображать не надо.
    Также можно использовать эту информацию при построении графа.

    """
    connections = await crud.entities_types_connections.get_many(db, limit=1000)
    return [EntitiesTypesConnectionInfo.from_orm(x) for x in connections]


@types_connections_router.get(
    '/info/{connection_id}',
    response_model=EntitiesTypesConnectionInfoExtended,
    response_class=ORJSONResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': ConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def get_connection_info(
        connection_id: int,
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Возвращает информацию о связи между типами сущностей
    вместе со списком связей самих сущностей. Требует статус editor.
    """
    cached = await cache.get_entities_types_connection(
        connection_id, redis_cursor
    )
    if cached is not None:
        return ORJSONResponse(cached.dict())

    connection = await crud.entities_types_connections.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionNotFoundResponse().detail
        )
    return ORJSONResponse(
        EntitiesTypesConnectionInfoExtended
        .from_orm(connection)
        .dict()
    )


@types_connections_router.post(
    '/create',
    response_model=EntitiesTypesConnectionInfo,
    responses={
        400: {'model': ConnectionCreatesCycleErrorResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        409: {'model': ConnectionAlreadyExistsResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_connection(
        create_form: EntitiesTypesConnectionCreate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает связь между типами сущностей. Требует статус admin."""
    connections = await crud.entities_types_connections.get_all(db)
    for connection in connections:
        if connection.parent_type == create_form.child_type \
                and connection.child_type == create_form.parent_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ConnectionAlreadyExistsResponse().detail
            )

    connections.append(EntitiesTypesConnection(parent_type=create_form.parent_type, child_type=create_form.child_type))
    if have_cycle(connections):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConnectionCreatesCycleErrorResponse().detail
        )

    try:
        connection = await crud.entities_types_connections.create(db, create_form)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ConnectionAlreadyExistsResponse().detail
        )

    await crud.change_log.log_create_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        element_id=connection.id
    )
    asyncio.create_task(cache.update_cache())
    return EntitiesTypesConnectionInfo.from_orm(connection)


@types_connections_router.put(
    '/update_name/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': ConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_column_name(
        connection_id: int,
        update_form: EntitiesTypesConnectionUpdate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет название колонки связей в таблице.

    Если указать null, колонка скроется.
    Требует статус admin.

    """
    connection = await crud.entities_types_connections.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionNotFoundResponse().detail
        )

    old_instance = dict(connection.__dict__)
    await crud.entities_types_connections.update(db, connection_id, update_form)

    await crud.change_log.log_update_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        update_form=update_form,
        old_instance=old_instance,
        new_instance=connection
    )
    asyncio.create_task(cache.update_cache())
    return OkResponse()


@types_connections_router.delete(
    '/delete/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': ConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_connection(
        connection_id: int,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Удаляет связь между типами сущностей. Требует статус admin."""
    connection = await crud.entities_types_connections.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionNotFoundResponse().detail
        )

    delete_log = await crud.change_log.log_delete_operation(
        db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        element_instance=connection
    )
    for entities_connection in connection.entities_connections:
        await crud.change_log.log_delete_operation(
            db,
            editor_id=editor_id,
            table=ChangedTable.ENTITIES_CONNECTIONS,
            element_instance=entities_connection,
            parent_change_id=delete_log.id
        )

    await crud.entities_types_connections.delete(db, connection_id)
    await cache.remove_entities_types_connections(connection_id, redis_cursor)
    asyncio.create_task(cache.update_cache())
    return OkResponse()
