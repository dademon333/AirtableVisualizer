from datetime import datetime

from pydantic import BaseModel

from infrastructure.db import ChangeType, ChangedTable


class ChangeLogDBInsertDTO(BaseModel):
    editor_id: int
    type: ChangeType
    table: ChangedTable
    element_id: int
    parent_change_id: int | None = None


class ChangeLogDBUpdateDTO(BaseModel):
    pass


class ChangeLogOutputDTO(BaseModel):
    id: int
    editor_id: int
    type: ChangeType
    table: ChangedTable
    element_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class DBElementUpdateDBInsertDTO(BaseModel):
    column: str
    old_value: str | None
    new_value: str | None
    change_id: int


class DBElementUpdateDBUpdateDTO(BaseModel):
    pass


class DBElementUpdateOutputDTO(BaseModel):
    column: str
    old_value: str | None
    new_value: str | None

    class Config:
        orm_mode = True


class ArchivedDBElementDBInsertDTO(BaseModel):
    element_data: dict
    change_id: int


class ArchivedDBElementDBUpdateDTO(BaseModel):
    pass


class ArchivedDBElementOutputDTO(BaseModel):
    element_data: dict

    class Config:
        orm_mode = True
