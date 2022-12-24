from fastapi import APIRouter, Depends

from auth.di import get_login_use_case, check_auth, get_logout_use_case, \
    oauth2_scheme
from auth.dto import LoginInputDTO, LoginOutputDTO
from auth.exceptions import LoginErrorResponse, UnauthorizedResponse
from auth.use_cases.login import LoginUseCase
from auth.use_cases.logout import LogoutUseCase
from common.responses import OkResponse

auth_router = APIRouter()


@auth_router.post(
    '/login',
    response_model=LoginOutputDTO,
    responses={403: {'model': LoginErrorResponse}}
)
async def login(
        input_dto: LoginInputDTO,
        use_case: LoginUseCase = Depends(get_login_use_case),
):
    """Endpoint авторизации.

    Если все окей, возвращает access token. Срок жизни сессии - 30 дней.

    """
    return await use_case.execute(input_dto)


@auth_router.delete(
    '/logout',
    response_model=OkResponse,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)]
)
async def logout(
        access_token: str | None = Depends(oauth2_scheme),
        use_case: LogoutUseCase = Depends(get_logout_use_case),
):
    """Удаляет информацию о авторизационной сессии на сервере."""
    await use_case.execute(access_token)
    return OkResponse()
