import asyncio

import sqlalchemy.exc
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud, cache
from common.db import UserStatus, get_db, ChangedTable
from common.responses import OkResponse, UnauthorizedResponse, EditorStatusRequiredResponse
from common.schemas.entities_connections import EntitiesConnectionCreate
from common.security.auth import UserStatusChecker, get_user_id
from .schemas import EntityNotFoundResponse, TypesConnectionNotFoundResponse, \
    EntitiesConnectionForm, ConnectionAlreadyExists, EntitiesConnectionNotFoundResponse

entities_connections_router = APIRouter()


@entities_connections_router.post(
    '/connect',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntityNotFoundResponse | TypesConnectionNotFoundResponse},
        409: {'model': ConnectionAlreadyExists}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def connect_entities(
        connect_form: EntitiesConnectionForm,
        db: AsyncSession = Depends(get_db),
        editor_id: int = Depends(get_user_id)
):
    """Создает связь между сущностями. Требует статус editor."""
    parent_entity = await crud.entities.get_by_id(db, connect_form.parent_id)
    child_entity = await crud.entities.get_by_id(db, connect_form.child_id)

    if parent_entity is None or child_entity is None:
        if parent_entity is None:
            not_found_id = connect_form.parent_id
        else:
            not_found_id = connect_form.child_id

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=EntityNotFoundResponse(entity_id=not_found_id).dict()
        )

    types_connection = await crud.entities_types_connections.get_by_types(
        db, parent_entity.type, child_entity.type
    )
    if types_connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TypesConnectionNotFoundResponse().detail
        )

    try:
        new_connection = await crud.entities_connections.create(
            db,
            EntitiesConnectionCreate(
                parent_id=connect_form.parent_id,
                child_id=connect_form.child_id,
                types_connection_id=types_connection.id
            )
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ConnectionAlreadyExists().detail
        )
    else:
        await crud.change_log.log_create_operation(
            db,
            editor_id=editor_id,
            table=ChangedTable.ENTITIES_CONNECTIONS,
            element_id=new_connection.id
        )
        asyncio.create_task(cache.update_cache())

    return OkResponse()


@entities_connections_router.delete(
    '/disconnect',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
        404: {'model': EntitiesConnectionNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def disconnect_entities(
        connect_form: EntitiesConnectionForm,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет связь между сущностями. Требует статус editor."""
    connection = await crud.entities_connections.get_by_entities(
        db, connect_form.parent_id, connect_form.child_id
    )
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntitiesConnectionNotFoundResponse().detail
        )

    await crud.entities_connections.delete(db, connection.id)
    await crud.change_log.log_delete_operation(
        db,
        editor_id=editor_id,
        table=ChangedTable.ENTITIES_CONNECTIONS,
        element_instance=connection
    )
    asyncio.create_task(cache.update_cache())
    return OkResponse()
