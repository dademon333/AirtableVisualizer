from pydantic import BaseModel, Field

from infrastructure.db import EntityType, EntitySize



class CreateEntityInputDTO(BaseModel):
    name: str
    type: EntityType
    size: EntitySize = EntitySize.MEDIUM
    description: str | None
    study_time: int | None = Field(
        None, description='Время освоения (в часах)'
    )

    class Config:
        orm_mode = True


class EntityDBInsertDTO(CreateEntityInputDTO):
    id: int | None


class UpdateEntityInputDTO(BaseModel):
    name: str | None
    size: EntitySize | None
    description: str | None
    study_time: int | None = Field(
        None,
        description='Время освоения (в часах)'
    )


class EntityDBUpdateDTO(UpdateEntityInputDTO):
    pass


class EntityOutputDTO(BaseModel):
    id: int
    name: str
    type: EntityType
    size: EntitySize = EntitySize.MEDIUM
    description: str | None
    study_time: int | None = Field(
        None, description='Время освоения (в часах)'
    )

    class Config:
        orm_mode = True
