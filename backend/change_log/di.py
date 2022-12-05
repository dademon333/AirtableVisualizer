from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from change_log.archived_db_elements_repository import \
    ArchivedDBElementsRepository
from change_log.change_log_repository import ChangeLogRepository
from change_log.db_element_updates_repository import DBElementUpdatesRepository
from change_log.facade import ChangeLogFacade
from infrastructure.db import get_db


def get_change_log_repository(
        db: AsyncSession = Depends(get_db),
) -> ChangeLogRepository:
    return ChangeLogRepository(db)


def get_db_element_updates_repository(
        db: AsyncSession = Depends(get_db),
) -> DBElementUpdatesRepository:
    return DBElementUpdatesRepository(db)


def get_archived_db_elements_repository(
        db: AsyncSession = Depends(get_db),
) -> ArchivedDBElementsRepository:
    return ArchivedDBElementsRepository(db)


def get_change_log_facade(
        change_log_repository: ChangeLogRepository = Depends(
            get_change_log_repository
        ),
        db_element_updates_repository: DBElementUpdatesRepository = Depends(
            get_db_element_updates_repository
        ),
        archived_db_elements_repository: ArchivedDBElementsRepository = Depends(  # noqa
            get_archived_db_elements_repository
        ),
) -> ChangeLogFacade:
    return ChangeLogFacade(
        change_log_repository,
        db_element_updates_repository,
        archived_db_elements_repository,
    )
