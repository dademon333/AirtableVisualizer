from users.dto import UserOutputDTO
from users.repository import UserRepository


class GetUserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.repository = repository

    async def execute(self, user_id: int) -> UserOutputDTO | None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None
        return UserOutputDTO.from_orm(user)
