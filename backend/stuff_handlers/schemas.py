from pydantic import BaseModel



class LoginForm(BaseModel):
    email: str
    password: str



class HostnameResponse(BaseModel):
    hostname: str


class LoginErrorResponse(BaseModel):
    detail: str = 'invalid email or password'
