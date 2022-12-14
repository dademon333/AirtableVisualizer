import sqlalchemy.exc

from users.dto import UserOutputDTO, UserDBInsertDTO, CreateUserInputDTO
from users.exceptions import UserEmailAlreadyUsedError
from users.repository import UserRepository


class CreateUserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.repository = repository

    async def execute(self, input_dto: CreateUserInputDTO) -> UserOutputDTO:
        try:
            user = await self.repository.insert(
                UserDBInsertDTO(**input_dto.dict())
            )
        except sqlalchemy.exc.IntegrityError:
            raise UserEmailAlreadyUsedError()

        return UserOutputDTO.from_orm(user)
