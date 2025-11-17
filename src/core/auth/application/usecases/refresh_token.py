import uuid

from src.api.auth.auth_dto import RefreshTokenDTO, LoginResponseDTO
from src.core.auth.application.abstract_auth_uow import AbstractIdentityUnitOfWork
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError, TokenCryptographyError
from src.core.auth.infrastructure.exceptions.exception_classes import InvalidTokenError, TokenExpiredError
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService


class RefreshTokenUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIdentityUnitOfWork,
        token_service: AbstractTokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, refresh_data: RefreshTokenDTO):
        try:
            payload = self.token_service.verify_token(refresh_data.refresh_token, TokenTypeEnum.REFRESH_TOKEN)
            user_id_from_jwt = uuid.UUID(payload.get("sub"))

        except (TokenExpiredError, InvalidTokenError) as exc:
            raise TokenCryptographyError(
                code="token_cryptography_error",
            ) from exc

        async with self.unit_of_work as uow:
            identity = await uow.identity.find_by_token_value(refresh_data.refresh_token)
            if not identity:
                raise TokenStateError(code="token_state_error")

            if identity.user_id != user_id_from_jwt:
                raise TokenStateError(code="token_state_error")

            identity.revoke_token(refresh_data.refresh_token)
            await uow.identity.save(identity)

            user_id = identity.user_id
            access_token = self.token_service.create_auth_token(user_id=user_id, token_type=TokenTypeEnum.ACCESS_TOKEN)
            refresh_token = self.token_service.create_auth_token(user_id=user_id, token_type=TokenTypeEnum.REFRESH_TOKEN)

            identity.add_new_token(
                token_type=refresh_token.token_type,
                token_value=refresh_token.token_value,
                expires_at=refresh_token.expires_at
            )

            await uow.identity.save(identity)
            await uow.commit()

        return LoginResponseDTO(
            access_token=access_token.token_value,
            refresh_token=refresh_token.token_value
        )


