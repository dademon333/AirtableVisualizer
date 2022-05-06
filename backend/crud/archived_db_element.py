from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import ArchivedDbElement, ChangedTable, ChangeLog
from schemas.archived_db_element import ArchivedDbElementCreate, ArchivedDbElementUpdate
from .base import CRUDBase


class CRUDArchivedDbElement(CRUDBase[ArchivedDbElement, ArchivedDbElementCreate, ArchivedDbElementUpdate]):
    # noinspection PyMethodMayBeStatic
    async def search(
            self,
            db: AsyncSession,
            table: ChangedTable,
            ids: list[int]
    ) -> list[ArchivedDbElement]:
        result = await db.scalars(
            select(ArchivedDbElement)
            .join(ChangeLog)
            .where(
                (ChangeLog.element_id.in_(ids))  # noqa
                & (ChangeLog.table == table)
            )
            .distinct(ChangeLog.element_id)
            .order_by(ChangeLog.element_id, ChangeLog.id.desc())  # noqa
        )
        return result.unique().all()


archived_db_element = CRUDArchivedDbElement(ArchivedDbElement)
