from typing import NoReturn

from auth.repository import AuthRepository


class LogoutUseCase:
    def __init__(
            self,
            auth_repository: AuthRepository,
    ):
        self.auth_repository = auth_repository

    async def execute(self, access_token: str) -> NoReturn:
        await self.auth_repository.delete_session(access_token)
