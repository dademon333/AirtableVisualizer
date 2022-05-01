import socket

from fastapi import APIRouter, Depends

from common.security import UserStatusChecker
from db import UserStatus
from .schemas import HostnameResponse

stuff_router = APIRouter()


@stuff_router.get(
    '/hostname',
    response_model=HostnameResponse,
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def get_hostname():
    """Возвращает hostname сервера(контейнера), в котором запущен код.
    Можно использовать для проверки работы вертикального масштабирования,
    хотя в основном используется для тестов во время разработки.
    """
    return HostnameResponse(hostname=socket.gethostname())
