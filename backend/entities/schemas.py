from pydantic import BaseModel


class EntityNotFoundResponse(BaseModel):
    detail: str = 'Entity not found'
