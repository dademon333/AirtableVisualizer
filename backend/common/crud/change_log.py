from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.sqlalchemy_modules import convert_instance_to_dict
from common.db import ChangeLog, ChangeType, ChangedTable
from common.schemas.archived_db_elements import ArchivedDbElementCreate
from common.schemas.change_log import ChangeLogCreate, ChangeLogUpdate
from common.schemas.db_elements_updates import DbElementUpdateCreate
from .archived_db_elements import archived_db_elements
from .base import Base, CRUDBase
from .db_elements_updates import db_elements_updates


class CRUDChangeLog(CRUDBase[ChangeLog, ChangeLogCreate, ChangeLogUpdate]):
    async def get_many(
            self,
            db: AsyncSession,
            limit: int = 100,
            offset: int = 0,
            exclude_admin_tables: bool = True
    ) -> list[ChangeLog]:
        if exclude_admin_tables:
            where_clause = (
                (ChangeLog.parent_change_id == None)  # noqa: E711
                & (ChangeLog.table.not_in([
                    ChangedTable.USERS, ChangedTable.ENTITIES_TYPES_CONNECTIONS
                ]))
            )
        else:
            where_clause = ChangeLog.parent_change_id == None  # noqa: E711

        result = await db.scalars(
            select(ChangeLog)
            .where(where_clause)
            .order_by(ChangeLog.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()

    async def log_create_operation(
            self,
            db: AsyncSession,
            editor_id: int,
            table: ChangedTable,
            element_id: int
    ) -> ChangeLog:
        return await self.create(
            db,
            ChangeLogCreate(
                editor_id=editor_id,
                type=ChangeType.CREATE,
                table=table,
                element_id=element_id
            )
        )

    async def log_update_operation(
            self,
            db: AsyncSession,
            editor_id: int,
            table: ChangedTable,
            update_form: BaseModel,
            old_instance: dict[str, Any],
            new_instance: Base
    ) -> ChangeLog | None:
        log_instance = None

        for key, value in update_form.dict().items():
            if old_instance[key] == getattr(new_instance, key):
                continue
            if table == ChangedTable.USERS and key == 'password':
                continue

            log_instance = await self.create(
                db,
                ChangeLogCreate(
                    editor_id=editor_id,
                    type=ChangeType.UPDATE,
                    table=table,
                    element_id=new_instance.id
                )
            )
            await db_elements_updates.create(
                db,
                DbElementUpdateCreate(
                    column=key,
                    old_value=old_instance[key],
                    new_value=getattr(new_instance, key),
                    change_id=log_instance.id
                )
            )
        return log_instance

    async def log_delete_operation(
            self,
            db: AsyncSession,
            editor_id: int,
            table: ChangedTable,
            element_instance: Base,
            parent_change_id: int | None = None
    ) -> ChangeLog:
        log_record = await self.create(
            db,
            ChangeLogCreate(
                editor_id=editor_id,
                type=ChangeType.DELETE,
                table=table,
                element_id=element_instance.id,
                parent_change_id=parent_change_id
            )
        )

        element_data = convert_instance_to_dict(element_instance)
        await archived_db_elements.create(
            db,
            ArchivedDbElementCreate(
                element_data=element_data,
                change_id=log_record.id
            )
        )
        return log_record


change_log = CRUDChangeLog(ChangeLog)
