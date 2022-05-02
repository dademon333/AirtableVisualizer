from pydantic import BaseModel, Field

from db import UserStatus


class UserCreate(BaseModel):
    name: str
    email: str = Field(..., regex=r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z')
    password: str = Field(..., min_length=8, max_length=30)
    status: UserStatus


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = Field(None, regex=r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z')
    password: str | None = Field(None, min_length=8, max_length=30)
    status: UserStatus | None = None


class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    status: UserStatus

    class Config:
        orm_mode = True
