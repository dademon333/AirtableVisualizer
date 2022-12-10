from fastapi import HTTPException, status
from pydantic import BaseModel

from infrastructure.db import UserStatus


class UnauthorizedResponse(BaseModel):
    detail: str = 'Unauthorized'


class EditorStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum editor status'


class AdminStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum admin status'


class NotEnoughRightsResponse(BaseModel):
    detail: str = 'Not enough rights'


class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)


class LowStatusError(HTTPException):
    def __init__(self, min_status: UserStatus):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'This operation requires minimum {min_status} status'
        )
