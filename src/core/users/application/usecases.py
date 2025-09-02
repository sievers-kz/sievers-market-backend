from src.api.users.user_dto import UserDTO, IndividualUserDTO, BusinessUserDTO, UserAuthDTO
from src.core.users.infrastructure.factories import UserFactory
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher


class RegisterUserUseCase:
    def __init__(self, user_repo: AbstractRepository, hasher: BcryptPasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    async def execute(self, user_dto: UserDTO):
        user_aggregate = UserFactory.create(user_dto)
        await self.user_repo.save(user_aggregate)

