import uuid

from src.api.users.user_dto import ResetPasswordDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork
from src.core.shared.infrastructure.services.password_hasher import BcryptPasswordHasher, AbstractPasswordHasher
from src.core.users.application.exceptions.exception_classes import InternalServerError


class ResetPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserIdentityUnitOfWork,
        token_service: AbstractTokenService,
        password_hasher: AbstractPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.password_hasher = password_hasher

    async def execute(self, reset_password_dto: ResetPasswordDTO):
        payload = self.token_service.verify_token(reset_password_dto.reset_password_token, TokenTypeEnum.PASSWORD_RESET_TOKEN)
        user_id_from_jwt = uuid.UUID(payload.get("sub"))

        async with self.unit_of_work as uow:
            identity = await uow.identity.find_by_token_value(reset_password_dto.reset_password_token)
            if not identity:
                raise TokenStateError(code="token_state_error")

            if identity.user_id != user_id_from_jwt:
                raise TokenStateError(code="token_state_error")

            identity.revoke_token(reset_password_dto.reset_password_token)

            new_hashed_password = self.password_hasher.hash_password(reset_password_dto.new_password)
            identity.reset_password(new_hashed_password)

            await uow.identity.save(identity)
            await uow.commit()