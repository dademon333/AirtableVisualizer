from pydantic import BaseModel

from entities.dto import EntityOutputDTO
from entity_connections.dto import EntityConnectionOutputDTO


class CourseOutputDTO(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        orm_mode = True


class CourseWithConnectionsOutputDTO(CourseOutputDTO):
    entities: list[EntityOutputDTO]
    entity_connections: list[EntityConnectionOutputDTO]


class CoursesWithConnectionsOutputDTO(BaseModel):
    courses: list[EntityOutputDTO]
    entities: list[EntityOutputDTO]
    entity_connections: list[EntityConnectionOutputDTO]
