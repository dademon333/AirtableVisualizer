from users.dto import UserOutputDTO
from users.repository import UserRepository


class ListUsersUseCase:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.repository = repository

    async def execute(
            self,
            limit: int = 250,
            offset: int = 0,
    ) -> list[UserOutputDTO]:
        users = await self.repository.get_many(limit=limit, offset=offset)
        return [UserOutputDTO.from_orm(x) for x in users]
