import uuid
from typing import Tuple

from src.api.users.user_dto import UserDTO, IndividualUserDTO, BusinessUserDTO, UserAuthDTO, LoginUserDTO, \
    LoginResponseDTO, TokenDataDTO
from src.core.users.domain.entities import UserAggregate
from src.core.users.infrastructure.factories import UserFactory, AuthTokenFactory
from src.core.users.domain.interfaces import AbstractRepository
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.users.infrastructure.user_repository import AuthTokenRepository


class RegisterUserUseCase:
    def __init__(self, user_repo: AbstractRepository, hasher: BcryptPasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    async def execute(self, user_dto: UserDTO):
        user_aggregate = UserFactory.create(user_dto)
        await self.user_repo.save(user_aggregate)


class LoginUserUseCase:
    def __init__(
        self,
        user_repo: AbstractRepository,
        token_service: PyJWTTokenService,
        token_repository: AuthTokenRepository
    ):
        self.user_repo = user_repo
        self.token_service = token_service
        self.token_repository = token_repository

    async def execute(self, login_data: LoginUserDTO):
        """Этот метод я разнес по нескольким приватным методам"""
        user = await self._get_validated_user(login_data)
        access_token, refresh_token = self._create_token_pair(user)
        await self._persist_refresh_token(user.id, refresh_token)
        return self._build_response(access_token, refresh_token)

    async def _get_validated_user(self, login_data: LoginUserDTO):
        user = await self.user_repo.get_by_email(login_data.email)
        if not user:
            raise ValueError("Пользователя с таким email не существует!")

        password = user.authentication.password
        is_match = password.matches(login_data.password)

        if not is_match:
            raise ValueError("Неправильный пароль!")

        return user

    def _create_token_pair(self, user: UserAggregate) -> Tuple[TokenDataDTO, TokenDataDTO]:
        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)
        return access_token, refresh_token

    async def _persist_refresh_token(self, user_id: uuid.UUID, refresh_token: TokenDataDTO):
        refresh_token_aggregate = AuthTokenFactory.create_refresh_token(
            user_id=user_id,
            token_value=refresh_token.token_str,
            expires_at=refresh_token.expires_at
        )
        await self.token_repository.save(refresh_token_aggregate)

    def _build_response(self, access_token: TokenDataDTO, refresh_token: TokenDataDTO) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=access_token.token_str,
            refresh_token=refresh_token.token_str
        )


