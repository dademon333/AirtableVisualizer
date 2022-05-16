import asyncio

import sqlalchemy.exc
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud, cache
from common.responses import UnauthorizedResponse, EditorStatusRequiredResponse, \
    OkResponse, AdminStatusRequiredResponse
from common.security.auth import UserStatusChecker, get_user_status
from common.sqlalchemy_modules import convert_instance_to_dict
from common.db import UserStatus, get_db, ChangeType, ChangedTable
from common.schemas.db_elements_updates import DbElementUpdateInfo
from common.schemas.users import UserInfo
from .modules import find_elements_data, convert_to_info_model, revert_delete_change, \
    revert_update_change, revert_create_change
from .schemas import ChangeLogRecord, ChangeLogNotFoundResponse, CantRevertChangeResponse

change_log_router = APIRouter()


@change_log_router.get(
    '/list',
    response_model=list[ChangeLogRecord],
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse}
    },
    response_model_exclude_unset=True,
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def list_changes(
        limit: int = 100,
        offset: int = 0,
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db),
):
    """Возвращает историю изменений бд.

    Для редакторов не показывает изменения в таблицах users и entities_types_connections.
    Требует статус editor.

    """
    changes = await crud.change_log.get_many(
        db,
        limit,
        offset,
        exclude_admin_tables=user_status != UserStatus.ADMIN
    )
    elements_data = await find_elements_data(db, changes)

    result = []
    for change in changes:
        element_data = elements_data[change.table][change.element_id]
        change_data = convert_instance_to_dict(change)

        if change.editor_data is not None:
            editor_data = UserInfo.from_orm(change.editor_data)
        else:
            editor_data = None
            del change_data['editor_data']

        log_record = ChangeLogRecord(
            **change_data,
            editor_data=editor_data,
            element_data=convert_to_info_model(element_data, change.table)
        )
        if change.type == ChangeType.UPDATE:
            log_record.update_info = DbElementUpdateInfo.from_orm(change.update_instance)

        result.append(log_record)

    return result


@change_log_router.delete(
    '/revert/change_id',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse | AdminStatusRequiredResponse},
        404: {'model': ChangeLogNotFoundResponse},
        409: {'model': CantRevertChangeResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def revert_change(
        change_id: int,
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Откатывает изменения бд по их идентификаторам.

    Откат изменений в таблицах users и entities_types_connections требует статус admin.
    Требует статус editor.

    """
    change_data = await crud.change_log.get_by_id(db, change_id)

    if change_data is None or change_data.parent_change_id is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ChangeLogNotFoundResponse().detail
        )

    if user_status is UserStatus.EDITOR \
            and change_data.table in [ChangedTable.USERS, ChangedTable.ENTITIES_TYPES_CONNECTIONS]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=AdminStatusRequiredResponse().detail
        )

    try:
        match change_data.type:
            case ChangeType.CREATE:
                await revert_create_change(db, change_data)
            case ChangeType.UPDATE:
                await revert_update_change(db, change_data)
            case ChangeType.DELETE:
                await revert_delete_change(db, change_data)
                for dependent in change_data.dependent_changes:
                    await revert_delete_change(db, dependent)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=CantRevertChangeResponse().detail
        )

    await crud.change_log.delete(db, change_data.id)
    asyncio.create_task(cache.update_cache())
    return OkResponse()
