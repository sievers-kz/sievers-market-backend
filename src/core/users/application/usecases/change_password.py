import uuid

from src.api.users.user_dto import ChangePasswordDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.application.abstract_uow import AbstractUserIdentityUnitOfWork
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher


class ChangePasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserIdentityUnitOfWork,
        token_service: AbstractTokenService,
        password_hasher: AbstractPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.password_hasher = password_hasher

    async def execute(self, change_password_dto: ChangePasswordDTO):
        payload = self.token_service.verify_token(change_password_dto.access_token, TokenTypeEnum.ACCESS_TOKEN)
        user_id = uuid.UUID(payload.get("sub"))

        async with self.unit_of_work as uow:
            identity = await uow.identity.get_user_identity(user_id)
            old_password = change_password_dto.old_password
            current_password = identity.credentials.hashed_password.hashed_password

            password_is_matches = self.password_hasher.verify_password(old_password, current_password)
            if not password_is_matches:
                raise InvalidCredentialsError(code="invalid_credentials_error")

            new_hashed_password = self.password_hasher.hash_password(change_password_dto.new_password)
            identity.change_password(new_hashed_password)

            await uow.identity.save(identity)
            await uow.commit()
