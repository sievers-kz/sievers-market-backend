from src.api.iam.dto import ResetPasswordData
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.domain.enums import TokenType
from src.core.iam.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher


class ResetPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        token_service: AbstractTokenService,
        password_hasher: AbstractPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.password_hasher = password_hasher

    async def execute(self, reset_password_data: ResetPasswordData):
        try:
            self.token_service.verify_token(reset_password_data.password_reset_token, TokenType.PASSWORD)
        except Exception:
            raise ValueError("Invalid reset password token")

        async with self.unit_of_work as uow:
            account = await uow.account.find_by_token_value(reset_password_data.password_reset_token)
            if not account:
                raise ValueError("Token not found")

            new_hashed_password = self.password_hasher.hash_password(reset_password_data.raw_password)
            account.reset_password(reset_password_data.password_reset_token, new_hashed_password)

            await uow.account.save(account)
            await uow.commit()
