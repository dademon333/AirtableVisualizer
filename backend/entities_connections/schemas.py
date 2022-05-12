from pydantic import BaseModel


class EntitiesConnectionForm(BaseModel):
    parent_id: int
    child_id: int


class EntityNotFoundResponse(BaseModel):
    detail: str = 'Entity not found'
    entity_id: int


class ConnectionAlreadyExists(BaseModel):
    detail: str = 'This connection already exists'


class EntitiesConnectionNotFoundResponse(BaseModel):
    detail: str = 'Entities connection not found'


class TypesConnectionNotFoundResponse(BaseModel):
    detail: str = 'Such entities types connection not found'
