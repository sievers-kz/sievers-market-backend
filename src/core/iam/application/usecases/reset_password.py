from src.core.iam.application.services.otp import OTPService
from src.core.iam.presentation.dto import ResetPasswordData
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.domain.enums import OTPType
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher


class ResetPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        password_hasher: AbstractPasswordHasher,
        otp_service: OTPService,
    ):
        self.unit_of_work = unit_of_work
        self.password_hasher = password_hasher
        self.otp_service = otp_service

    async def execute(self, reset_password_data: ResetPasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(reset_password_data.email)
            if not account:
                raise ValueError("Пользователь не найден")

            await self.otp_service.verify(
                account_id=account.id,
                otp_type=OTPType.PASSWORD_RESET,
                otp_value=reset_password_data.password_reset_otp,
            )

            new_hashed_password = self.password_hasher.hash_password(reset_password_data.raw_password)
            account.reset_password(new_hashed_password)

            await uow.account.save(account)
            await uow.commit()

