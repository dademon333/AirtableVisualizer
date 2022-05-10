import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from common.responses import OkResponse, UnauthorizedResponse, AdminStatusRequiredResponse
from common.security.auth import UserStatusChecker, get_user_id
from db import UserStatus, get_db, ChangedTable, EntitiesTypesConnection
from entities_types_connections.modules import have_cycle
from entities_types_connections.schemas import ConnectionNotFoundResponse, \
    ConnectionCreateErrorResponse, ConnectionCreatesCycleErrorResponse
from schemas.entities_types_connections import EntitiesTypesConnectionUpdate, CoursesEntitiesTypesConnectionInfo, \
    EntitiesTypesConnectionCreate

types_connections_router = APIRouter()


@types_connections_router.get(
    '/list',
    response_model=list[CoursesEntitiesTypesConnectionInfo]
)
async def list_connections(
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о связях между типами сущностей.
    На основе этой информации необходимо строить колонки связей в таблицах.
    Если в названии колонки указан null, её отображать не надо.
    Также можно использовать эту информацию при построении графа.
    """
    return await crud.entities_types_connections.get_many(db, limit=1000)


@types_connections_router.post(
    '/create',
    response_model=CoursesEntitiesTypesConnectionInfo,
    responses={
        400: {'model': ConnectionCreateErrorResponse | ConnectionCreatesCycleErrorResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_connection(
        create_form: EntitiesTypesConnectionCreate,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает связь между типами сущностей.
    Требует статус admin.
    """
    connections = await crud.entities_types_connections.get_all(db)
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConnectionCreateErrorResponse().detail
        )

    await crud.change_log.log_create_operation(
        db=db,
        editor_id=user_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        element_id=connection.id
    )
    return CoursesEntitiesTypesConnectionInfo.from_orm(connection)


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
        user_id: int = Depends(get_user_id),
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
        editor_id=user_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        update_form=update_form,
        old_instance=old_instance,
        new_instance=connection
    )
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
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет связь между типами сущностей.
    Требует статус admin.
    """
    connection = await crud.entities_types_connections.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionNotFoundResponse().detail
        )

    delete_log = await crud.change_log.log_delete_operation(
        db,
        editor_id=user_id,
        table=ChangedTable.ENTITIES_TYPES_CONNECTIONS,
        element_instance=connection
    )
    for entities_connection in connection.entities_connections:
        await crud.change_log.log_delete_operation(
            db,
            editor_id=user_id,
            table=ChangedTable.ENTITIES_CONNECTIONS,
            element_instance=entities_connection,
            parent_change_id=delete_log.id
        )

    await crud.entities_types_connections.delete(db, connection_id)
    return OkResponse()
