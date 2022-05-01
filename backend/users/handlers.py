from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from common.project_cookies import ProjectCookies
from common.redis import get_redis_cursor
from common.security import hash_password, get_user_id, check_auth, UserStatusChecker
from db import get_db, UserStatus
from .schemas import LoginForm, LoginErrorResponse, UserInfo, OkResponse, UserNotFoundResponse

users_router = APIRouter()


@users_router.post(
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
    user = await crud.user.get_by_email(db, form_data.email)

    if user is not None:
        hashed_password = hash_password(user.id, form_data.password)
        if hashed_password == user.password:
            session_id = await crud.user_session.create(user.id, redis_cursor)
            response = JSONResponse(UserInfo.from_orm(user).dict())
            response.set_cookie(key=ProjectCookies.SESSION_ID.value, value=session_id)
            return response

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=LoginErrorResponse().detail
    )


@users_router.post('/logout', response_model=OkResponse)
async def logout(
        redis_cursor: Redis = Depends(get_redis_cursor),
        session_id: str = Cookie(default=None, include_in_schema=False)
):
    """Адрес этого endpoint'а дает исчерпывающую информацию о его предназначении.
    Удаляет cookie 'session_id' и информацию о сессии на сервере.
    """
    response = JSONResponse(OkResponse().dict())
    response.delete_cookie(key=ProjectCookies.SESSION_ID.value)
    await crud.user_session.delete(session_id, redis_cursor)
    return response


@users_router.get(
    '/info/me',
    response_model=UserInfo,
    dependencies=[Depends(check_auth)]
)
async def get_self_info(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_user_id)
):
    """Возвращает информацию о текущем пользователе."""
    user = await crud.user.get_by_id(db, user_id)
    return UserInfo.from_orm(user)


@users_router.get(
    '/info/{user_id}',
    response_model=UserInfo,
    responses={404: {'model': UserNotFoundResponse}},
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def get_user_info(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о пользователе по его id. Требует статус admin или выше."""
    user = await crud.user.get_by_id(db, user_id)
    if user is not None:
        return UserInfo.from_orm(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )
