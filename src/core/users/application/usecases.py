import uuid
from datetime import datetime, timedelta, timezone
from typing import Tuple

from src.api.users.user_dto import UserDTO, LoginUserDTO, LoginResponseDTO, TokenDataDTO, EmailConfirmationDTO
from src.core.users.application.uow import AbstractUserUnitOfWork
from src.core.users.domain.entities import UserAggregate
from src.core.users.infrastructure.factories import UserFactory, AuthTokenFactory
from src.core.users.infrastructure.services.email_sender import ConsoleEmailSender
from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService


class RegisterUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        sender: ConsoleEmailSender, # FIXME: Use some abstraction interface (AbstractEmailSender)
        token_service: PyJWTTokenService # FIXME: Use some abstraction interface (AbstractTokenService)
    ):
        self.unit_of_work = unit_of_work
        self.sender = sender
        self.token_service = token_service

    async def execute(self, user_dto: UserDTO):
        async with self.unit_of_work as uow:
            user = UserFactory.create(user_dto)
            await uow.user.save(user)

            token, code = await self._create_confirmation_code(user)
            await uow.token.save(token)

            await uow.commit()

        await self.sender.send_confirmation_email(to=user.email.value, code=code)

    async def _create_confirmation_code(self, user):
        code = self.token_service.create_confirmation_code()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        token_entity = AuthTokenFactory.create_email_token(
            user_id=user.id,
            expires_at=expires_at,
            token_value=code
        )
        return token_entity, code


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        token_service: PyJWTTokenService, # FIXME: Use some abstraction interface for clean (AbstractTokenService)
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

        if not user.is_active:
            raise ValueError("Вы все еще не подтвердили email!")

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


class EmailConfirmationUseCase:
    def __init__(self, unit_of_work: AbstractUserUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, confirmation_data: EmailConfirmationDTO):
        async with self.unit_of_work as uow:
            token = await uow.token.find_by_value(confirmation_data.confirmation_code)
            if not token:
                raise ValueError("Wrong confirmation code!")

            if token.is_expired():
                raise ValueError("Confirmation code expired!")

            user = await uow.user.get_by_id(token.user_id)
            user.confirm_email()
            await uow.user.save(user)
            await uow.commit()
