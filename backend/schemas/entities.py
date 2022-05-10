from pydantic import BaseModel, Field

from db import EntityType, EntitySize
from .entities_types_connections import CoursesEntitiesTypesConnectionInfo


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


class CourseInfo(EntityBase):
    id: int
    connections: list[CoursesEntitiesTypesConnectionInfo]
    entities: list[EntityInfo]


class CoursesSetInfo(BaseModel):
    connections: list[CoursesEntitiesTypesConnectionInfo]
    entities: list[EntityInfo]
