from fastapi import HTTPException, status
from pydantic import BaseModel


class UserNotFoundResponse(BaseModel):
    detail: str = 'User not found'


class UserEmailAlreadyUsedResponse(BaseModel):
    detail: str = 'Email already used'


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )


class UserEmailAlreadyUsedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=UserEmailAlreadyUsedResponse().detail
        )
