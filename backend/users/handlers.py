import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from common.responses import OkResponse, UnauthorizedResponse, AdminStatusRequiredResponse
from common.security.auth import get_user_id, check_auth, UserStatusChecker
from db import get_db, UserStatus, ChangedTable
from schemas.users import UserCreate, UserUpdate, UserInfo, UserInfoExtended
from .schemas import UserNotFoundResponse, UserEmailAlreadyExistsResponse, UserSelfUpdateForm

users_router = APIRouter()


@users_router.get(
    '/info/me',
    response_model=UserInfo,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)]
)
async def get_self_info(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_user_id)
):
    """Возвращает информацию о текущем пользователе."""
    user = await crud.users.get_by_id(db, user_id)
    return UserInfo.from_orm(user)


@users_router.get(
    '/info/{user_id}',
    response_model=UserInfo,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def get_user_info(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о пользователе по его id. Требует статус admin."""
    user = await crud.users.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )
    return UserInfo.from_orm(user)



@users_router.post(
    '/create',
    response_model=UserInfo,
    responses={
        400: {'model': UserEmailAlreadyExistsResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def create_user(
        create_form: UserCreate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает нового пользователя. Требует статус admin."""
    try:
        user = await crud.users.create(db, create_form)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UserEmailAlreadyExistsResponse().detail
        )

    await crud.change_log.log_create_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.USERS,
        element_id=user.id
    )
    return UserInfo.from_orm(user)


@users_router.put(
    '/update/me',
    response_model=OkResponse,
    responses={
        400: {'model': UserEmailAlreadyExistsResponse},
        401: {'model': UnauthorizedResponse}
    },
    dependencies=[Depends(check_auth)]
)
async def update_self(
        update_form: UserSelfUpdateForm,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о текущем пользователе. Все поля в теле запроса являются необязательными,
    передавать нужно только необходимые дня обновления.
    """
    user = await crud.users.get_by_id(db, user_id)
    old_instance = dict(user.__dict__)

    try:
        await crud.users.update(db, user_id, update_form)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UserEmailAlreadyExistsResponse().detail
        )

    await crud.change_log.log_update_operation(
        db=db,
        editor_id=user_id,
        table=ChangedTable.USERS,
        update_form=update_form,
        old_instance=old_instance,
        new_instance=user
    )
    return OkResponse()


@users_router.put(
    '/update/{user_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_user(
        user_id: int,
        update_form: UserUpdate,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о пользователе. Все поля в теле запроса являются необязательными,
    передавать нужно только необходимые дня обновления. Требует статус admin.
    """
    user = await crud.users.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )

    old_instance = dict(user.__dict__)
    try:
        await crud.users.update(db, user_id, update_form)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UserEmailAlreadyExistsResponse().detail
        )

    await crud.change_log.log_update_operation(
        db=db,
        editor_id=editor_id,
        table=ChangedTable.USERS,
        update_form=update_form,
        old_instance=old_instance,
        new_instance=user
    )
    return OkResponse()


@users_router.delete(
    '/delete/{user_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_user(
        user_id: int,
        editor_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет пользователя. Требует статус admin."""
    user = await crud.users.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )
    await crud.users.delete(db, user_id)
    await crud.change_log.log_delete_operation(
        db,
        editor_id=editor_id,
        table=ChangedTable.USERS,
        element_instance=user
    )
    return OkResponse()


@users_router.get(
    '/list',
    response_model=list[UserInfoExtended],
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def list_users(
        limit: int = Query(100, le=1000),
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о всех пользователях. Требует статус admin."""
    users = await crud.users.get_many(db, limit, offset)
    return [UserInfoExtended.from_orm(x) for x in users]
