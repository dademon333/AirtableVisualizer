from fastapi.responses import JSONResponse

from auth.repository import AuthRepository
from common.cookie import ProjectCookies
from common.responses import OkResponse


class LogoutUseCase:
    def __init__(
            self,
            auth_repository: AuthRepository,
    ):
        self.auth_repository = auth_repository

    async def execute(self, session_id: str) -> JSONResponse:
        response = JSONResponse(OkResponse().dict())
        response.delete_cookie(key=ProjectCookies.SESSION_ID.value)  # noqa
        await self.auth_repository.delete_session(session_id)
        return response
