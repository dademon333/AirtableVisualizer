from pydantic import BaseModel, Field

from entity_connections.dto import EntityConnectionOutputDTO
from infrastructure.db import EntityType


class EntityTypeConnectionDBInsertDTO(BaseModel):
    id: int | None
    parent_type: EntityType = Field(
        ..., description='Родительский тип сущности (из него выходят стрелки)'
    )
    child_type: EntityType = Field(
        ..., description='Дочерний тип сущности (в него входят стрелки)'
    )
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40,
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40,
    )

    class Config:
        orm_mode = True


class EntityTypeConnectionDBUpdateDTO(BaseModel):
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40,
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40,
    )


class CreateTypeConnectionInputDTO(BaseModel):
    parent_type: EntityType = Field(
        ..., description='Родительский тип сущности (из него выходят стрелки)'
    )
    child_type: EntityType = Field(
        ..., description='Дочерний тип сущности (в него входят стрелки)'
    )
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40,
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40,
    )

    class Config:
        orm_mode = True


class UpdateTypeConnectionInputDTO(BaseModel):
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40,
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40,
    )



class TypeConnectionOutputDTO(BaseModel):
    id: int
    parent_type: EntityType = Field(
        ..., description='Родительский тип сущности (из него выходят стрелки)'
    )
    child_type: EntityType = Field(
        ..., description='Дочерний тип сущности (в него входят стрелки)'
    )
    parent_column_name: str | None = Field(
        None,
        description='Название родительской колонки в дочерней таблице',
        max_length=40,
    )
    child_column_name: str | None = Field(
        None,
        description='Название дочерней колонки в родительской таблице',
        max_length=40,
    )

    class Config:
        orm_mode = True


class TypeConnectionExtendedOutputDTO(TypeConnectionOutputDTO):
    entity_connections: list[EntityConnectionOutputDTO]
