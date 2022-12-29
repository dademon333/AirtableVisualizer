import socket

from fastapi import Depends, APIRouter
from fastapi.responses import PlainTextResponse
from pympler import muppy, summary
import tracemalloc

from auth.di import UserStatusChecker
from auth.exceptions import UnauthorizedResponse, EditorStatusRequiredResponse
from infrastructure.db import UserStatus
from stuff_handlers.dto import HostnameOutputDTO

stuff_router = APIRouter()


@stuff_router.get(
    '/api/hostname',
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


@stuff_router.get(
    '/api/tracemalloc',
    response_class=PlainTextResponse
)
async def get_tracemalloc():
    snapshot = tracemalloc.take_snapshot()
    return '\n'.join(str(x) for x in snapshot.statistics('filename'))


@stuff_router.get(
    '/api/memory',
    response_class=PlainTextResponse
)
async def get_memory_usage():
    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)
    return '\n'.join(summary.format_(sum1))
