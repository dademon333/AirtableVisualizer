from sqlalchemy.ext.asyncio import AsyncSession

import crud
from common.sqlalchemy_modules import convert_instance_to_dict
from db import ChangeLog, ChangedTable, Base
from schemas.entities_connection import EntitiesConnectionInfo
from schemas.entities_types_connection import EntitiesTypesConnectionInfo, EntitiesTypesConnectionUpdate
from schemas.user import UserInfo, UserUpdate


async def find_elements_data(
        db: AsyncSession,
        changes: list[ChangeLog]
) -> dict[ChangedTable, dict[int, dict]]:
    """Searches data of changed elements among their native tables and archived elements"""
    result: dict[ChangedTable, dict[int, dict]] = {}
    to_search: dict[ChangedTable, set[int]] = {}

    for change in changes:
        if change.table not in to_search:
            to_search[change.table] = set()
        to_search[change.table].add(change.element_id)

    for table, ids in to_search.items():
        elements = await _search_elements_with_crud(db, table, ids)
        elements = [convert_instance_to_dict(x) for x in elements]

        archived_elements = await crud.archived_db_element.search(
            db=db,
            table=table,
            ids=ids - set(x['id'] for x in elements)
        )
        elements += [x.element_data for x in archived_elements]

        if len(elements) != len(ids):
            not_found = ids - set(x['id'] for x in elements)
            raise ValueError(f"find_elements_data can't find {not_found} ids from {table}")
        result[table] = {x['id']: x for x in elements}

    return result


async def _search_elements_with_crud(
        db: AsyncSession,
        table: ChangedTable,
        ids: set[int]
) -> list[Base]:
    match table:
        case ChangedTable.USERS:
            return await crud.user.get_by_ids(db, ids)
        case ChangedTable.ENTITIES_TYPES_CONNECTIONS:
            return await crud.entities_types_connection.get_by_ids(db, ids)
        case ChangedTable.ENTITIES_CONNECTIONS:
            return await crud.entities_connection.get_by_ids(db, ids)
        case _:
            raise NotImplementedError(f"Table '{table}' handle not implemented")


def convert_to_info_model(
        element_data: dict,
        table: ChangedTable
) -> UserInfo \
        | EntitiesTypesConnectionInfo \
        | EntitiesConnectionInfo:
    match table:
        case ChangedTable.USERS:
            return UserInfo(**element_data)
        case ChangedTable.ENTITIES_TYPES_CONNECTIONS:
            return EntitiesTypesConnectionInfo(**element_data)
        case ChangedTable.ENTITIES_CONNECTIONS:
            return EntitiesConnectionInfo(**element_data)
        case _:
            raise NotImplementedError(f"Table '{table}' handle not implemented")


async def revert_create_change(db: AsyncSession, change_data: ChangeLog) -> None:
    match change_data.table:
        case ChangedTable.USERS:
            return await crud.user.delete(db, change_data.element_id)
        case ChangedTable.ENTITIES_TYPES_CONNECTIONS:
            return await crud.entities_types_connection.delete(db, change_data.element_id)
        case ChangedTable.ENTITIES_CONNECTIONS:
            return await crud.entities_connection.delete(db, change_data.element_id)
        case _:
            raise NotImplementedError(f"Table '{change_data.table}' handle not implemented")


async def revert_update_change(db: AsyncSession, change_data: ChangeLog) -> None:
    arg = {change_data.update_instance.column: change_data.update_instance.old_value}
    match change_data.table:
        case ChangedTable.USERS:
            return await crud.user.update(
                db,
                change_data.element_id,
                UserUpdate(**arg)
            )
        case ChangedTable.ENTITIES_TYPES_CONNECTIONS:
            return await crud.entities_types_connection.update(
                db,
                change_data.element_id,
                EntitiesTypesConnectionUpdate(**arg)
            )
        case ChangedTable.ENTITIES_CONNECTIONS:
            raise ValueError(f'can\'t change entities connections table, '
                             f'change_id: {change_data.id}')
        case _:
            raise NotImplementedError(f"Table '{change_data.table}' handle not implemented")



async def revert_delete_change(db: AsyncSession, change_data: ChangeLog) -> None:
    element_data = change_data.delete_instance.element_data
    match change_data.table:
        case ChangedTable.USERS:
            return await crud.user.create_from_dict(db, element_data)
        case ChangedTable.ENTITIES_TYPES_CONNECTIONS:
            return await crud.entities_types_connection.create_from_dict(db, element_data)
        case ChangedTable.ENTITIES_CONNECTIONS:
            return await crud.entities_connection.create_from_dict(db, element_data)
        case _:
            raise NotImplementedError(f"Table '{change_data.table}' handle not implemented")
