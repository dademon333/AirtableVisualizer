from sqlalchemy import select

from change_log.dto import ArchivedDBElementDBUpdateDTO, \
    ArchivedDBElementDBInsertDTO
from infrastructure.db import BaseRepository, ArchivedDBElement, \
    ChangedTable, ChangeLog


class ArchivedDBElementsRepository(
    BaseRepository[
        ArchivedDBElement,
        ArchivedDBElementDBInsertDTO,
        ArchivedDBElementDBUpdateDTO,
    ]
):
    model = ArchivedDBElement

    async def search(
            self,
            table: ChangedTable,
            ids: list[int]
    ) -> list[ArchivedDBElement]:
        result = await self.db.scalars(
            select(ArchivedDBElement)
            .join(ChangeLog)
            .where(
                (ChangeLog.element_id.in_(ids))
                & (ChangeLog.table == table)
            )
            .distinct(ChangeLog.element_id)
            .order_by(ChangeLog.element_id, ChangeLog.id.desc())
        )
        return result.unique().all()
