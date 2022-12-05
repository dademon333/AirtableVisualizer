from pydantic import BaseModel, Field

from infrastructure.db import UserStatus


_EMAIL_REGEX = r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z'


class UserInsertDTO(BaseModel):
    id: int | None
    name: str
    email: str = Field(..., regex=_EMAIL_REGEX)
    password: str = Field(..., min_length=8, max_length=30)
    status: UserStatus

    class Config:
        orm_mode = True


class UserUpdateDTO(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=_EMAIL_REGEX)
    password: str | None = Field(None, min_length=8, max_length=30)
    status: UserStatus | None = None
