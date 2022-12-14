from fastapi import APIRouter, Depends, Query
from fastapi.responses import ORJSONResponse

from auth.di import UserStatusChecker, get_user_id, check_auth
from auth.exceptions import UnauthorizedResponse, AdminStatusRequiredResponse
from common.responses import OkResponse
from infrastructure.db import UserStatus
from users.di import get_list_users_use_case, get_get_user_use_case, \
    get_create_user_use_case, get_update_user_use_case, \
    get_delete_user_use_case
from users.dto import UserOutputDTO, CreateUserInputDTO, \
    UserSelfUpdateInputDTO, UserUpdateInputDTO
from users.exceptions import UserNotFoundResponse, UserNotFoundError, \
    UserEmailAlreadyUsedResponse
from users.use_cases.create_user import CreateUserUseCase
from users.use_cases.delete_user import DeleteUserUseCase
from users.use_cases.get_user import GetUserUseCase
from users.use_cases.list_users import ListUsersUseCase
from users.use_cases.update_user import UpdateUserUseCase

users_router = APIRouter()


@users_router.get(
    '/list',
    response_model=list[UserOutputDTO],
    response_class=ORJSONResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))],
)
async def list_users(
        limit: int = Query(250, le=1000),
        offset: int = 0,
        use_case: ListUsersUseCase = Depends(get_list_users_use_case),
):
    """Возвращает информацию о всех пользователях. Требует статус admin."""
    result = await use_case.execute(limit=limit, offset=offset)
    return ORJSONResponse([x.dict() for x in result])


@users_router.get(
    '/me',
    response_model=UserOutputDTO,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)],
)
async def get_self_info(
        user_id: int = Depends(get_user_id),
        use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    """Возвращает информацию о текущем пользователе."""
    return await use_case.execute(user_id)


@users_router.get(
    '/{user_id}',
    response_model=UserOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))],
)
async def get_user_info(
        user_id: int,
        use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    """Возвращает о пользователе по идентификатору."""
    result = await use_case.execute(user_id)
    if not result:
        raise UserNotFoundError()
    return result


@users_router.post(
    '',
    response_model=UserOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        409: {'model': UserEmailAlreadyUsedResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))],
)
async def create_user(
        input_dto: CreateUserInputDTO,
        use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    """Создает нового пользователя. Требует статус admin."""
    return await use_case.execute(input_dto)


@users_router.put(
    '/me',
    response_model=UserOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        409: {'model': UserEmailAlreadyUsedResponse}
    },
    dependencies=[Depends(check_auth)],
)
async def update_self(
        input_dto: UserSelfUpdateInputDTO,
        user_id: int = Depends(get_user_id),
        use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
):
    """Обновляет данные о текущем пользователе.

    Все поля в теле запроса являются необязательными, передавать нужно
    только необходимые дня обновления.

    """
    return await use_case.execute(user_id, input_dto)


@users_router.put(
    '/{user_id}',
    response_model=UserOutputDTO,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse},
        409: {'model': UserEmailAlreadyUsedResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))],
)
async def update_user(
        user_id: int,
        input_dto: UserUpdateInputDTO,
        use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
):
    """Обновляет данные о пользователе.

    Все поля в теле запроса являются необязательными, передавать нужно
    только необходимые дня обновления. Требует статус admin.

    """
    return await use_case.execute(user_id, input_dto)


@users_router.delete(
    '/{user_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))],
)
async def delete_user(
        user_id: int,
        use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
):
    """Удаляет пользователя. Требует статус admin."""
    await use_case.execute(user_id)
    return OkResponse()
