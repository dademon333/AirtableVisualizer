from pydantic import BaseModel

from db import UserStatus


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    status: UserStatus


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    status: UserStatus | None = None
