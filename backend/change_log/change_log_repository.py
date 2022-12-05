from sqlalchemy import select

from change_log.dto import ChangeLogDBInsertDTO, ChangeLogDBUpdateDTO
from infrastructure.db import BaseRepository, ChangeLog, ChangedTable


class ChangeLogRepository(
    BaseRepository[ChangeLog, ChangeLogDBInsertDTO, ChangeLogDBUpdateDTO]
):
    model = ChangeLog

    async def get_many(
            self,
            limit: int = 100,
            offset: int = 0,
            exclude_admin_tables: bool = True
    ) -> list[ChangeLog]:
        where_clause = ChangeLog.parent_change_id == None  # noqa: ignore=E711 (Comparison to None)
        if exclude_admin_tables:
            where_clause &= (
                ChangeLog.table.not_in([
                    ChangedTable.USERS, ChangedTable.ENTITIES_TYPES_CONNECTIONS
                ])
            )

        result = await self.db.scalars(
            select(ChangeLog)
            .where(where_clause)
            .order_by(ChangeLog.id)
            .limit(limit)
            .offset(offset)
        )
        return result.unique().all()
