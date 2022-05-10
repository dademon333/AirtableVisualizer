from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import ArchivedDbElement, ChangedTable, ChangeLog
from schemas.archived_db_elements import ArchivedDbElementCreate, ArchivedDbElementUpdate
from .base import CRUDBase


class CRUDArchivedDbElements(CRUDBase[ArchivedDbElement, ArchivedDbElementCreate, ArchivedDbElementUpdate]):
    @staticmethod
    async def search(
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


archived_db_elements = CRUDArchivedDbElements(ArchivedDbElement)
