import uuid

from src.api.users.user_dto import ResetPasswordDTO
from src.core.users.application.exceptions.exception_classes import InternalServerError, ServiceUnavailableError
from src.core.users.application.uow import AbstractUserUnitOfWork
from src.core.users.domain.entities import AuthTokenAggregate, UserAggregate
from src.core.users.domain.enums import TokenTypeEnum
from src.core.users.domain.exceptions.exception_classes import TokenCryptographyError, TokenStateError

from src.core.users.infrastructure.exceptions.exception_classes import (
    RepositoryError,
    TokenGeneratorService,
    UnitOfWorkError,
    DatabaseConnectionError,
    TokenExpiredError,
    InvalidTokenError
)

from src.core.users.infrastructure.services.pyjwt_token import PyJWTTokenService


class ResetPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        token_service: PyJWTTokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, reset_password_dto: ResetPasswordDTO):
        payload = self._validate_token_cryptography(reset_password_dto)
        user_id_from_jwt = self._extract_user_id(payload)

        try:
            async with self.unit_of_work as uow:
                db_token = await uow.token.find_by_value(reset_password_dto.reset_password_token)
                self._validate_token_state(db_token, user_id_from_jwt)

                user = await self._get_user(db_token, uow)
                user.change_password(reset_password_dto.new_password)
                await uow.user.save(user)

                db_token.revoke_token()
                await uow.token.save(db_token)

                await self._revoke_all_refresh_tokens(user.id, uow)
                await uow.commit()

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

    def _validate_token_cryptography(self, token_data: ResetPasswordDTO):
        try:
            payload = self.token_service.verify_token(token_data.reset_password_token, TokenTypeEnum.PASSWORD_RESET_TOKEN)
            if not payload:
                raise TokenCryptographyError(code="token_cryptography_error")
            return payload

        except TokenExpiredError as exc:
            raise TokenCryptographyError(
                code="token_cryptography_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

        except InvalidTokenError as exc:
            raise TokenCryptographyError(
                code="token_cryptography_error",
                details=exc.meta.details,
                context=exc.meta.context
            ) from exc

    def _validate_token_state(self, db_token, user_id_from_jwt):
        if not db_token:
            raise TokenStateError(code="token_state_error")

        if db_token.is_revoked:
            raise TokenStateError(code="token_state_error")

        if db_token.user_id != user_id_from_jwt:
            raise TokenStateError(code="token_state_error")

    def _extract_user_id(self, payload: dict) -> uuid.UUID:
        sub = payload.get("sub")
        if not sub:
            raise TokenCryptographyError(code="token_cryptography_error")
        return uuid.UUID(sub)

    async def _get_user(self, db_token: AuthTokenAggregate, uow: AbstractUserUnitOfWork) -> UserAggregate:
        user = await uow.user.get_by_id(db_token.user_id)
        if not user:
            raise InternalServerError(
                code="internal_server_error",
                details="Не удалось найти пользователя в базе данных",
            )

        return user

    async def _revoke_all_refresh_tokens(self, user_id: uuid.UUID, uow: AbstractUserUnitOfWork):
        active_refresh_tokens = await uow.token.find_all_refresh_tokens_by_user_id(user_id)
        for token in active_refresh_tokens:
            token.revoke_token()
            await uow.token.save(token)
