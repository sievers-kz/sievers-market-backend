import uuid
from typing import Tuple

from src.api.users.user_dto import UserDTO, LoginUserDTO, LoginResponseDTO, TokenDataDTO
from src.core.users.application.uow import AbstractUserUnitOfWork
from src.core.users.domain.entities import UserAggregate
from src.core.users.infrastructure.factories import UserFactory, AuthTokenFactory
from src.core.users.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService


class RegisterUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        hasher: BcryptPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.hasher = hasher

    async def execute(self, user_dto: UserDTO):
        async with self.unit_of_work as uow:
            user = UserFactory.create(user_dto)
            await uow.user.save(user)
            await uow.commit()


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        token_service: PyJWTTokenService,
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, login_data: LoginUserDTO):
        """Этот метод я разнес по нескольким приватным методам"""
        async with self.unit_of_work as uow:
            user = await self._get_validated_user(login_data, uow)
            access_token, refresh_token = self._create_token_pair(user)
            await self._persist_refresh_token(user.id, refresh_token, uow)
            await uow.commit()
        return self._build_response(access_token, refresh_token)

    async def _get_validated_user(self, login_data: LoginUserDTO, uow: AbstractUserUnitOfWork):
        user = await uow.user.get_by_email(login_data.email)
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

    async def _persist_refresh_token(
        self,
        user_id: uuid.UUID,
        refresh_token: TokenDataDTO,
        uow: AbstractUserUnitOfWork
    ):
        refresh_token_aggregate = AuthTokenFactory.create_refresh_token(
            user_id=user_id,
            token_value=refresh_token.token_str,
            expires_at=refresh_token.expires_at
        )
        await uow.token.save(refresh_token_aggregate)

    def _build_response(self, access_token: TokenDataDTO, refresh_token: TokenDataDTO) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=access_token.token_str,
            refresh_token=refresh_token.token_str
        )


