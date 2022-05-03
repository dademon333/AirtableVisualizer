from pydantic import BaseModel


class EntitiesTypesConnectionNotFoundResponse(BaseModel):
    detail: str = 'connection not found'


class EntitiesTypesConnectionCreateErrorResponse(BaseModel):
    detail: str = 'connection already exists'
