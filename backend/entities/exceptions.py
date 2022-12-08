from fastapi import HTTPException, status
from pydantic import BaseModel


class EntityNotFoundResponse(BaseModel):
    detail: str = 'Entity not found'


class EntityNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntityNotFoundResponse().detail,
        )
