import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

import crud
from common.responses import OkResponse
from common.security.auth import get_user_id, check_auth, UserStatusChecker
from db import get_db, UserStatus
from schemas.user import UserCreate, UserUpdate, UserInfo
from .schemas import UserNotFoundResponse, UserRegistrationErrorResponse

users_router = APIRouter()


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


@users_router.post(
    '/create',
    response_model=UserInfo,
    responses={400: {'model': UserRegistrationErrorResponse}},
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_user(
        create_instance: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создает нового пользователя. Требует статус admin или выше."""
    try:
        user = await crud.user.create(db, create_instance)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UserRegistrationErrorResponse().detail
        )
    else:
        return UserInfo.from_orm(user)


@users_router.put(
    '/update/{user_id}',
    response_model=OkResponse,
    responses={404: {'model': UserNotFoundResponse}},
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_user(
        user_id: int,
        update_form: UserUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о пользователе. Требует статус admin или выше."""
    user = await crud.user.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )
    await crud.user.update(db, user_id, update_form)
    return OkResponse()


@users_router.delete(
    '/delete/{user_id}',
    response_model=OkResponse,
    responses={404: {'model': UserNotFoundResponse}},
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удаляет пользователя. Требует статус admin или выше."""
    user = await crud.user.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )
    await crud.user.delete(db, user_id)
    return OkResponse()
