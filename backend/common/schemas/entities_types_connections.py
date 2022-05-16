from pydantic import BaseModel, Field

from common.db import EntityType
from .entities_connections import EntitiesConnectionInfoReduced


class EntitiesTypesConnectionNamesBase(BaseModel):
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


class EntitiesTypesConnectionTypesBase(BaseModel):
    parent_type: EntityType = Field(..., description='Родительский тип сущности (из него выходят стрелки)')
    child_type: EntityType = Field(..., description='Дочерний тип сущности (в него входят стрелки)')


class EntitiesTypesConnectionFullBase(
    EntitiesTypesConnectionTypesBase,
    EntitiesTypesConnectionNamesBase
):
    pass


class EntitiesTypesConnectionCreate(EntitiesTypesConnectionFullBase):
    pass


class EntitiesTypesConnectionUpdate(EntitiesTypesConnectionNamesBase):
    pass


class EntitiesTypesConnectionInfo(EntitiesTypesConnectionFullBase):
    id: int

    class Config:
        orm_mode = True


class EntitiesTypesConnectionInfoExtended(EntitiesTypesConnectionTypesBase):
    """Special version for courses info."""

    id: int
    entities_connections: list[EntitiesConnectionInfoReduced]

    class Config:
        orm_mode = True
