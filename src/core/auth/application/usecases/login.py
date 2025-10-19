import uuid
from typing import Tuple

from src.api.users.user_dto import TokenDataDTO
from src.api.auth.auth_dto import LoginUserDTO, LoginResponseDTO
from src.core.auth.application.exceptions.exception_classes import InternalServerError, ServiceUnavailableError
from src.core.shared.application.abstract_uow import AbstractUserAuthUnitOfWork
from src.core.users.domain.entities import UserAggregate
from src.core.users.domain.exceptions.exception_classes import EmailNotConfirmedError
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError
from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError
from src.core.auth.infrastructure.exceptions.exception_classes import RepositoryError, TokenGeneratorService

from src.core.auth.infrastructure.factories import AuthTokenFactory
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService


class LoginUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserAuthUnitOfWork,
        token_service: PyJWTTokenService, # FIXME: Use some abstraction interface for clean (AbstractTokenService)
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, login_data: LoginUserDTO):
        """Этот метод я разнес по нескольким приватным методам"""
        try:
            async with self.unit_of_work as uow:
                user = await self._get_validated_user(login_data, uow)
                access_token, refresh_token = self._create_token_pair(user)
                await self._persist_refresh_token(user.id, refresh_token, uow)
                await uow.commit()
            return self._build_response(access_token, refresh_token)

        except (RepositoryError, TokenGeneratorService) as exc:
            raise InternalServerError(
                code="internal_server_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

        except (UnitOfWorkError, DatabaseConnectionError) as exc:
            raise ServiceUnavailableError(
                code="service_unavailable_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

    async def _get_validated_user(self, login_data: LoginUserDTO, uow: AbstractUserAuthUnitOfWork):
        user = await uow.user.get_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsError(code="invalid_login_credentials")

        password = user.authentication.password
        is_match = password.matches(login_data.password)

        if not is_match:
            raise InvalidCredentialsError(code="invalid_login_credentials")

        if not user.is_active:
            raise EmailNotConfirmedError(code="email_not_confirmed")

        return user

    def _create_token_pair(self, user: UserAggregate) -> Tuple[TokenDataDTO, TokenDataDTO]:
        access_token = self.token_service.create_access_token(user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)
        return access_token, refresh_token

    async def _persist_refresh_token(
        self,
        user_id: uuid.UUID,
        refresh_token: TokenDataDTO,
        uow: AbstractUserAuthUnitOfWork
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