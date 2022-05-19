import socket

from aioredis import Redis
from fastapi import APIRouter, Depends, Cookie, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.project_cookies import ProjectCookies
from common.redis import get_redis_cursor
from common.responses import OkResponse, UnauthorizedResponse, EditorStatusRequiredResponse
from common.security.auth import UserStatusChecker, check_auth
from common.security.users import hash_password
from common.db import UserStatus, get_db
from common.schemas.users import UserInfo
from .schemas import HostnameResponse, LoginErrorResponse, LoginForm

stuff_router = APIRouter()


@stuff_router.get(
    '/hostname',
    response_model=HostnameResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': EditorStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.EDITOR))]
)
async def get_hostname():
    """Возвращает hostname сервера(контейнера), в котором запущен код.

    Можно использовать для проверки работы вертикального масштабирования,
    хотя в основном используется для тестов во время разработки.

    """
    return HostnameResponse(hostname=socket.gethostname())


@stuff_router.post(
    '/login',
    response_model=UserInfo,
    responses={403: {'model': LoginErrorResponse}}
)
async def login(
        form_data: LoginForm,
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Адрес этого endpoint'а дает исчерпывающую информацию о его предназначении.

    Если все окей, устанавливает cookie 'session_id' и возвращает информацию о пользователе.
    Срок жизни сессии - 30 дней.

    """
    user = await crud.users.get_by_email(db, form_data.email)

    if user is not None:
        hashed_password = hash_password(user.id, form_data.password)
        if hashed_password == user.password:
            session_id = await crud.user_sessions.create(user.id, redis_cursor)
            response = JSONResponse(UserInfo.from_orm(user).dict())
            response.set_cookie(key=ProjectCookies.SESSION_ID.value, value=session_id)
            return response

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=LoginErrorResponse().detail
    )


@stuff_router.delete(
    '/logout',
    response_model=OkResponse,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)]
)
async def logout(
        redis_cursor: Redis = Depends(get_redis_cursor),
        session_id: str = Cookie(default=None, include_in_schema=False)
):
    """Адрес этого endpoint'а дает исчерпывающую информацию о его предназначении.

    Удаляет cookie 'session_id' и информацию о сессии на сервере.

    """
    response = JSONResponse(OkResponse().dict())
    response.delete_cookie(key=ProjectCookies.SESSION_ID.value)
    await crud.user_sessions.delete(session_id, redis_cursor)
    return response
