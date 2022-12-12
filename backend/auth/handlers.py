from fastapi import APIRouter, Depends, Cookie

from auth.di import get_login_use_case, check_auth, get_logout_use_case
from auth.dto import LoginInputDTO
from auth.exceptions import LoginErrorResponse, UnauthorizedResponse
from auth.use_cases.login import LoginUseCase
from auth.use_cases.logout import LogoutUseCase
from common.responses import OkResponse
from users.dto import UserOutputDTO

auth_router = APIRouter()


@auth_router.post(
    '/login',
    response_model=UserOutputDTO,
    responses={403: {'model': LoginErrorResponse}}
)
async def login(
        input_dto: LoginInputDTO,
        use_case: LoginUseCase = Depends(get_login_use_case),
):
    """Endpoint авторизации.

    Если все окей, устанавливает cookie 'session_id' и возвращает информацию
    о пользователе. Срок жизни сессии - 30 дней.

    """
    return await use_case.execute(input_dto)


@auth_router.delete(
    '/logout',
    response_model=OkResponse,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)]
)
async def logout(
        session_id: str = Cookie(default=None, include_in_schema=False),
        use_case: LogoutUseCase = Depends(get_logout_use_case),
):
    """Сбрасывает авторизацию пользователя.

    Удаляет cookie 'session_id' и информацию о сессии на сервере.

    """
    return await use_case.execute(session_id)
