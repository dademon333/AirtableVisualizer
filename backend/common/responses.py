from pydantic import BaseModel


class OkResponse(BaseModel):
    response: str = 'ok'


class UnauthorizedResponse(BaseModel):
    detail: str = 'Unauthorized'


class EditorStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum editor status'


class AdminStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum admin status'
