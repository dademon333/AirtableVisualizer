from datetime import datetime

from pydantic import BaseModel, Field

from infrastructure.db import UserStatus


_EMAIL_REGEX = r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z'


class UserDBInsertDTO(BaseModel):
    id: int | None
    name: str
    email: str = Field(..., regex=_EMAIL_REGEX)
    password: str = Field(..., min_length=8, max_length=30)
    status: UserStatus

    class Config:
        orm_mode = True


class UserDBUpdateDTO(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=_EMAIL_REGEX)
    password: str | None = Field(None, min_length=8, max_length=30)
    status: UserStatus | None = None


class UserOutputDTO(BaseModel):
    id: int
    name: str
    email: str
    status: UserStatus
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUserInputDTO(BaseModel):
    name: str
    email: str = Field(
        ...,
        regex=_EMAIL_REGEX
    )
    password: str = Field(..., min_length=8, max_length=30)
    status: UserStatus

    class Config:
        orm_mode = True


class UserSelfUpdateInputDTO(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=_EMAIL_REGEX)
    password: str | None = Field(None, min_length=8, max_length=30)


class UserUpdateInputDTO(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=_EMAIL_REGEX)
    password: str | None = Field(None, min_length=8, max_length=30)
    status: UserStatus | None = None
