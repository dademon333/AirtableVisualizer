import socket

from fastapi import Depends, APIRouter

from auth.di import UserStatusChecker
from auth.exceptions import UnauthorizedResponse, EditorStatusRequiredResponse
from infrastructure.db import UserStatus
from stuff_handlers.dto import HostnameOutputDTO

stuff_router = APIRouter()


@stuff_router.get(
    '/hostname',
    response_model=HostnameOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def get_hostname():
    """Возвращает hostname сервера(контейнера), в котором запущен код.

    В основном используется для тестов во время разработки.

    """
    return HostnameOutputDTO(hostname=socket.gethostname())
