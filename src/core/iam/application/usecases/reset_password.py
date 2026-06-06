from loguru import logger

from src.core.iam.application.interfaces.password_service import IPasswordService
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.exceptions import AccountNotFoundError
from src.core.iam.presentation.dto import ResetPasswordData
from src.core.iam.application.interfaces.uow import IIAMUnitOfWork
from src.core.iam.domain.enums import OTPType


class ResetPasswordUseCase:
    def __init__(
        self,
        unit_of_work: IIAMUnitOfWork,
        password_service: IPasswordService,
        otp_service: OTPService,
    ):
        self.unit_of_work = unit_of_work
        self.password_service = password_service
        self.otp_service = otp_service

    async def execute(self, reset_password_data: ResetPasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(reset_password_data.email)
            if not account:
                raise AccountNotFoundError()

            await self.otp_service.verify(
                account_id=account.id,
                otp_type=OTPType.PASSWORD_RESET,
                otp_value=reset_password_data.password_reset_otp,
            )

            self.password_service.validate(reset_password_data.raw_password)
            new_hashed_password = self.password_service.hash(reset_password_data.raw_password)
            account.reset_password(new_hashed_password)

            await uow.account.save(account)
            await uow.commit()

        logger.info("Password successfully reseted | account_id={}", account.id)