from fastapi import HTTPException, status
from pydantic import BaseModel


class TypeConnectionNotFoundResponse(BaseModel):
    detail: str = 'Such entity types connection not found'


class TypeConnectionAlreadyExistsResponse(BaseModel):
    detail: str = 'Types connection already exists'


class TypeConnectionNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TypeConnectionNotFoundResponse().detail
        )


class TypeConnectionAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=TypeConnectionAlreadyExistsResponse().detail
        )
