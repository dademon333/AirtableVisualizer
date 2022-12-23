from pydantic import BaseModel


class LoginInputDTO(BaseModel):
    email: str
    password: str


class LoginOutputDTO(BaseModel):
    access_token: str
    token_type: str = 'bearer'
