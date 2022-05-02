from pydantic import BaseModel, Field


class UserSelfUpdateForm(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z')
    password: str | None = Field(None, min_length=8, max_length=30)


class UserNotFoundResponse(BaseModel):
    detail: str = 'user not found'


class UserRegistrationErrorResponse(BaseModel):
    detail: str = 'email already exists'
