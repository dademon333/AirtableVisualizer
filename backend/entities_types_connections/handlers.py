import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from common.responses import OkResponse, UnauthorizedResponse, AdminStatusRequiredResponse
from common.security.auth import UserStatusChecker
from db import UserStatus, get_db
from entities_types_connections.schemas import EntitiesTypesConnectionNotFoundResponse, \
    EntitiesTypesConnectionCreateErrorResponse
from schemas.entities_types_connection import EntitiesTypesConnectionUpdate, EntitiesTypesConnectionInfo, \
    EntitiesTypesConnectionCreate

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
    return await crud.entities_types_connection.get_many(db, limit=1000)


@types_connections_router.post(
    '/create',
    response_model=EntitiesTypesConnectionInfo,
    responses={
        400: {'model': EntitiesTypesConnectionCreateErrorResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_connection(
        create_form: EntitiesTypesConnectionCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создает связь между типами сущностей.
    Требует статус admin.
    """
    # Проверка длины
    try:
        connection = await crud.entities_types_connection.create(db, create_form)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EntitiesTypesConnectionCreateErrorResponse().detail
        )
    else:
        return EntitiesTypesConnectionInfo.from_orm(connection)


@types_connections_router.put(
    '/update_name/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': EntitiesTypesConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_column_name(
        connection_id: int,
        update_form: EntitiesTypesConnectionUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновляет название колонки связей в таблице.
    Если указать null, колонка скроется.
    Требует статус admin.
    """
    connection = await crud.entities_types_connection.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntitiesTypesConnectionNotFoundResponse().detail
        )
    await crud.entities_types_connection.update(db, connection_id, update_form)
    return OkResponse()


@types_connections_router.delete(
    '/delete/{connection_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': EntitiesTypesConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_connection(
        connection_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удаляет связь между типами сущностей.
    Требует статус admin.
    """
    connection = await crud.entities_types_connection.get_by_id(db, connection_id)
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntitiesTypesConnectionNotFoundResponse().detail
        )
    await crud.entities_types_connection.delete(db, connection_id)
    return OkResponse()
