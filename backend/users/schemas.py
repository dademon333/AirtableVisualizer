from pydantic import BaseModel


class UserNotFoundResponse(BaseModel):
    detail: str = 'user not found'


class UserRegistrationErrorResponse(BaseModel):
    detail: str = 'email already exists'
