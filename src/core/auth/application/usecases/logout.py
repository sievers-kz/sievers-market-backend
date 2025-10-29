import uuid

from src.api.auth.auth_dto import RefreshTokenDTO
from src.core.auth.application.abstract_auth_uow import AbstractIdentityUnitOfWork
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService


class LogoutUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIdentityUnitOfWork,
        token_service: AbstractTokenService
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service

    async def execute(self, refresh_data: RefreshTokenDTO):
        payload = self.token_service.verify_token(refresh_data.refresh_token, TokenTypeEnum.REFRESH_TOKEN)
        user_id_from_jwt = uuid.UUID(payload.get("sub"))

        async with self.unit_of_work as uow:
            identity = await uow.identity.find_by_token_value(refresh_data.refresh_token)
            if not identity:
                raise TokenStateError(code="token_state_error")

            if identity.user_id != user_id_from_jwt:
                raise TokenStateError(code="token_state_error")

            identity.revoke_token(refresh_data.refresh_token)
            await uow.identity.save(identity)
            await uow.commit()
