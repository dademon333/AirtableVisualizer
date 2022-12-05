from typing import Any

from pydantic import BaseModel

from change_log.archived_db_elements_repository import \
    ArchivedDBElementsRepository
from change_log.change_log_repository import ChangeLogRepository
from change_log.db_element_updates_repository import DBElementUpdatesRepository
from change_log.dto import ChangeLogDBInsertDTO, DBElementUpdateDBInsertDTO, \
    ArchivedDBElementDBInsertDTO
from infrastructure.db import ChangedTable, ChangeLog, ChangeType, Base


class ChangeLogFacade:
    def __init__(
            self,
            change_log_repository: ChangeLogRepository,
            db_element_updates_repository: DBElementUpdatesRepository,
            archived_db_elements_repository: ArchivedDBElementsRepository,
    ):
        self._change_log_repository = change_log_repository
        self._db_element_updates_repository = db_element_updates_repository
        self._archived_db_elements_repository = archived_db_elements_repository

    async def log_create_operation(
            self,
            editor_id: int,
            table: ChangedTable,
            element_id: int
    ) -> ChangeLog:
        return await self._change_log_repository.insert(
            ChangeLogDBInsertDTO(
                editor_id=editor_id,
                type=ChangeType.CREATE,
                table=table,
                element_id=element_id
            )
        )

    async def log_update_operation(
            self,
            editor_id: int,
            table: ChangedTable,
            update_dto: BaseModel,
            old_instance: dict[str, Any],
            new_instance: Base
    ) -> ChangeLog | None:
        log_instance = None

        for key, value in update_dto.dict().items():
            if old_instance[key] == getattr(new_instance, key):
                continue
            if table == ChangedTable.USERS and key == 'password':
                continue

            log_instance = await self._change_log_repository.insert(
                ChangeLogDBInsertDTO(
                    editor_id=editor_id,
                    type=ChangeType.UPDATE,
                    table=table,
                    element_id=new_instance.id
                )
            )
            await self._db_element_updates_repository.insert(
                DBElementUpdateDBInsertDTO(
                    column=key,
                    old_value=old_instance[key],
                    new_value=getattr(new_instance, key),
                    change_id=log_instance.id
                )
            )
        return log_instance

    async def log_delete_operation(
            self,
            editor_id: int,
            table: ChangedTable,
            element_instance: Base,
            parent_change_id: int | None = None
    ) -> ChangeLog:
        log_record = await self._change_log_repository.insert(
            ChangeLogDBInsertDTO(
                editor_id=editor_id,
                type=ChangeType.DELETE,
                table=table,
                element_id=element_instance.id,
                parent_change_id=parent_change_id
            )
        )

        element_data = dict(element_instance.__dict__)
        del element_data['_sa_instance_state']
        await self._archived_db_elements_repository.insert(
            ArchivedDBElementDBInsertDTO(
                element_data=element_data,
                change_id=log_record.id
            )
        )
        return log_record
