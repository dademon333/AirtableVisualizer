from datetime import datetime

from pydantic import BaseModel

from common.db import ChangeType, ChangedTable


class ChangeLogCreate(BaseModel):
    editor_id: int
    type: ChangeType
    table: ChangedTable
    element_id: int
    parent_change_id: int | None = None


class ChangeLogUpdate(BaseModel):
    pass


class ChangeLogInfo(BaseModel):
    id: int
    editor_id: int
    type: ChangeType
    table: ChangedTable
    element_id: int
    created_at: datetime

    class Config:
        orm_mode = True
