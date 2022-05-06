from pydantic import BaseModel, Field

from db import EntityType


class EntitiesTypesConnectionBase(BaseModel):
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40
    )


class EntitiesTypesConnectionBaseExtended(EntitiesTypesConnectionBase):
    parent_type: EntityType = Field(..., description='Родительский тип сущности (из него выходят стрелки)')
    child_type: EntityType = Field(..., description='Дочерний тип сущности (в него входят стрелки)')


class EntitiesTypesConnectionCreate(EntitiesTypesConnectionBaseExtended):
    pass


class EntitiesTypesConnectionUpdate(EntitiesTypesConnectionBase):
    pass


class EntitiesTypesConnectionInfo(EntitiesTypesConnectionBaseExtended):
    id: int

    class Config:
        orm_mode = True
