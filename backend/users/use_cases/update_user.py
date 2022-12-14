import sqlalchemy.exc

from users.dto import UserOutputDTO, UserSelfUpdateInputDTO, UserDBUpdateDTO, \
    UserUpdateInputDTO
from users.exceptions import UserEmailAlreadyUsedError, UserNotFoundError
from users.repository import UserRepository


class UpdateUserUseCase:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.repository = repository

    async def execute(
            self,
            user_id: int,
            input_dto: UserSelfUpdateInputDTO | UserUpdateInputDTO
    ) -> UserOutputDTO:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        try:
            user = await self.repository.update(
                user_id,
                UserDBUpdateDTO(**input_dto.dict(exclude_unset=True))
            )
        except sqlalchemy.exc.IntegrityError:
            raise UserEmailAlreadyUsedError()

        return UserOutputDTO.from_orm(user)
