import uuid
from typing import Tuple

from src.api.users.user_dto import TokenDataDTO
from src.api.auth.auth_dto import LoginResponseDTO, RefreshTokenDTO
from src.core.auth.application.exceptions.exception_classes import ServiceUnavailableError, InternalServerError
from src.core.auth.application.abstract_auth_uow import AbstractAuthUnitOfWork
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError, TokenCryptographyError

from src.core.shared.infrastructure.exceptions.exception_classes import DatabaseConnectionError, UnitOfWorkError

from src.core.auth.infrastructure.exceptions.exception_classes import (
    TokenExpiredError,
    InvalidTokenError,
    RepositoryError,
    TokenGeneratorService
)

from src.core.auth.infrastructure.factories import AuthTokenFactory
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService


class RefreshTokenUseCase:
    def __init__(
        self,
        unit_of_work: AbstractAuthUnitOfWork,
        token_service: PyJWTTokenService
    ):
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

                user_id = db_token.user_id
                access_token, refresh_token = self._create_token_pair(user_id)

                token_aggregate = self._persist_refresh_token(user_id, refresh_token)
                await uow.token.save(token_aggregate)

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

    def _extract_user_id(self, payload: dict) -> uuid.UUID:
        sub = payload.get("sub")
        if not sub:
            raise TokenCryptographyError(code="token_cryptography_error")
        return uuid.UUID(sub)

    def _validate_token_state(self, db_token, user_id_from_jwt):
        if not db_token:
            raise TokenStateError(code="token_state_error")

        if db_token.is_revoked:
            raise TokenStateError(code="token_state_error")

        if db_token.user_id != user_id_from_jwt:
            raise TokenStateError(code="token_state_error")

    def _create_token_pair(self, user_id: uuid.UUID) -> Tuple[TokenDataDTO, TokenDataDTO]:
        access_token = self.token_service.create_access_token(user_id)
        refresh_token = self.token_service.create_refresh_token(user_id)
        return access_token, refresh_token

    def _persist_refresh_token(self, user_id: uuid.UUID, refresh_token: TokenDataDTO):
        return AuthTokenFactory.create_refresh_token(
            user_id=user_id,
            token_value=refresh_token.token_str,
            expires_at=refresh_token.expires_at
        )

    def _build_response(self, access_token: TokenDataDTO, refresh_token: TokenDataDTO) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=access_token.token_str,
            refresh_token=refresh_token.token_str
        )