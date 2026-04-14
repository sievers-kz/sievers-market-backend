import asyncio

from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import ForgotPasswordData
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork


class ForgotPasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        otp_service,
    ):
        self.unit_of_work = unit_of_work
        self.otp_service = otp_service

    async def execute(self, forgot_password_data: ForgotPasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(forgot_password_data.email)
            if not account:
                await asyncio.sleep(0.5)
                return

        await self.otp_service.send(
            account_id=account.id,
            email=account.email.value,
            otp_type=OTPType.PASSWORD_RESET,
        )
