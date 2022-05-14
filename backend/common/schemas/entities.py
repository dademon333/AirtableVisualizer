from pydantic import BaseModel, Field

from common.db import EntityType, EntitySize
from .entities_types_connections import EntitiesTypesConnectionInfoExtended


class EntityBase(BaseModel):
    name: str
    type: EntityType
    size: EntitySize = EntitySize.MEDIUM
    description: str | None = None
    study_time: int | None = Field(None, description='Время освоения (в часах)')


class EntityCreate(EntityBase):
    pass


class EntityUpdate(BaseModel):
    name: str | None = None
    size: EntitySize | None = None
    description: str | None = None
    study_time: int | None = Field(None, description='Время освоения (в часах)')


class EntityInfo(EntityBase):
    id: int

    class Config:
        orm_mode = True


class EntityInfoReduced(EntityBase):
    class Config:
        orm_mode = True


class CourseInfo(EntityBase):
    id: int
    connections: list[EntitiesTypesConnectionInfoExtended]
    entities: dict[str, EntityInfoReduced]


class CoursesSetInfo(BaseModel):
    connections: list[EntitiesTypesConnectionInfoExtended]
    entities: dict[str, EntityInfoReduced]
