from datetime import datetime

from pydantic import BaseModel, Field

from common.db import ChangeType, ChangedTable
from common.schemas.db_elements_updates import DbElementUpdateInfo
from common.schemas.entities_connections import EntitiesConnectionInfo
from common.schemas.entities_types_connections import EntitiesTypesConnectionInfo
from common.schemas.hidden_courses import HiddenCourseInfo
from common.schemas.users import UserInfo


class ChangeLogRecord(BaseModel):
    id: int
    type: ChangeType
    table: ChangedTable
    element_id: int
    created_at: datetime
    element_data: \
        UserInfo \
        | EntitiesTypesConnectionInfo \
        | EntitiesConnectionInfo \
        | HiddenCourseInfo \
        = Field(
            ...,
            description='Последняя найденная в бд информация об элементе'
        )
    editor_id: int | None
    editor_data: UserInfo | None = Field(
        ...,
        description='Информация о редакторе. Null, если редактор был удалён из бд.'
     )
    update_info: DbElementUpdateInfo | None = Field(
        None,
        description="Информация об обновлении элемента. "
                    "Указывается, если type=update"
    )


class CantRevertChangeResponse(BaseModel):
    detail: str = 'Can\'t revert this change'


class ChangeLogNotFoundResponse(BaseModel):
    detail: str = 'Change not found'
