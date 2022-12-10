from pydantic import BaseModel


class EntityConnectionInputDTO(BaseModel):
    parent_id: int
    child_id: int


class EntityConnectionDBInsertDTO(BaseModel):
    id: int | None
    parent_id: int
    child_id: int
    type_connection_id: int

    class Config:
        orm_mode = True


class EntityConnectionDBUpdateDTO(BaseModel):
    pass


class EntityConnectionOutputDTO(BaseModel):
    id: int
    parent_id: int
    child_id: int
    type_connection_id: int

    class Config:
        orm_mode = True
