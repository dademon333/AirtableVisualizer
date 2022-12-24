from auth.dto import LoginInputDTO, LoginOutputDTO
from auth.exceptions import LoginError
from auth.repository import AuthRepository
from auth.utils import hash_password
from users.repository import UserRepository


class LoginUseCase:
    def __init__(
            self,
            auth_repository: AuthRepository,
            user_repository: UserRepository,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    async def execute(self, input_dto: LoginInputDTO) -> LoginOutputDTO:
        user = await self.user_repository.get_by_email(input_dto.email)
        if not user:
            raise LoginError()

        hashed_password = hash_password(user.id, input_dto.password)
        if hashed_password != user.password:
            raise LoginError()

        access_token = await self.auth_repository.create_session(user.id)
        return LoginOutputDTO(access_token=access_token)
