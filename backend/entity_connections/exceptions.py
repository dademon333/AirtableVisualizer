from fastapi import HTTPException, status
from pydantic import BaseModel


class EntityConnectionAlreadyExistsResponse(BaseModel):
    detail: str = 'Connection already exists'


class EntityConnectionNotFoundResponse(BaseModel):
    detail: str = 'Connection not found'


class EntityConnectionAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=EntityConnectionAlreadyExistsResponse().detail
        )


class EntityConnectionNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EntityConnectionNotFoundResponse().detail
        )
