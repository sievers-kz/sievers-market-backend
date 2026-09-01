from loguru import logger

from src.core.iam.application.interfaces.uow import IIAMUnitOfWork
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import ResendCodeRequest


class ResendConfirmationCodeUseCase:
    def __init__(
        self,
        unit_of_work: IIAMUnitOfWork,
        otp_service: OTPService,
    ):
        self.unit_of_work = unit_of_work
        self.otp_service = otp_service

    async def execute(self, resend_data: ResendCodeRequest):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_email(resend_data.email)
            if not account:
                logger.info("Account not found | email={}", resend_data.email)
                return

        await self.otp_service.send(
            account_id=account.id,
            email=account.email.value,
            otp_type=OTPType.CONFIRMATION,
        )
