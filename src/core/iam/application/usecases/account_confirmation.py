from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import AccountConfirmation
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork


class AccountConfirmationUseCase:
    def __init__(self, unit_of_work: AbstractIAMUnitOfWork, otp_service: OTPService):
        self.unit_of_work = unit_of_work
        self.otp_service = otp_service

    async def execute(self, confirmation_data: AccountConfirmation):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_id(confirmation_data.account_id)
            if not account:
                raise ValueError("Invalid confirmation token")

            await self.otp_service.verify(
                account_id=account.id,
                otp_type=OTPType.CONFIRMATION,
                otp_value=confirmation_data.confirm_code,
            )

            account.confirm_account()
            await uow.account.save(account)
            await uow.commit()
