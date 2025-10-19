import uuid

from src.api.auth.auth_dto import RefreshTokenDTO
from src.core.auth.application.abstract_auth_uow import AbstractAuthUnitOfWork
from src.core.auth.application.exceptions.exception_classes import InternalServerError, ServiceUnavailableError
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenCryptographyError, TokenStateError

from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError

from src.core.auth.infrastructure.exceptions.exception_classes import (
    RepositoryError,
    TokenGeneratorService,
    TokenExpiredError,
    InvalidTokenError
)

from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService


class LogoutUserUseCase:
    def __init__(self, unit_of_work: AbstractAuthUnitOfWork, token_service: PyJWTTokenService):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, token_data: RefreshTokenDTO):
        payload = self._validate_token_cryptography(token_data)
        user_id_from_jwt = self._extract_user_id(payload)

        try:
            async with self.unit_of_work as uow:
                db_token = await uow.token.find_by_value(token_data.refresh_token)
                self._validate_token_state(db_token, user_id_from_jwt)

                db_token.revoke_token()
                await uow.token.save(db_token)
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

    def _validate_token_cryptography(self, token_data: RefreshTokenDTO):
        try:
            payload = self.token_service.verify_token(token_data.refresh_token, TokenTypeEnum.REFRESH_TOKEN)
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