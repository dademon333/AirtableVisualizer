from pydantic import BaseModel

from db import UserStatus


class LoginForm(BaseModel):
    email: str
    password: str


class OkResponse(BaseModel):
    response: str = 'ok'


class LoginErrorResponse(BaseModel):
    detail: str = 'invalid email or password'


class UserNotFoundResponse(BaseModel):
    detail: str = 'user not found'


class UserInfo(BaseModel):
    name: str
    email: str
    status: UserStatus

    class Config:
        orm_mode = True
