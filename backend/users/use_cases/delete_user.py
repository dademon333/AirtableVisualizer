from typing import NoReturn

from users.exceptions import UserNotFoundError
from users.repository import UserRepository


class DeleteUserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.repository = repository

    async def execute(self, user_id: int) -> NoReturn:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        await self.repository.delete(user_id)
