from uuid import UUID

from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.value_objects import Phone
from src.core.iam.presentation.dto import ConfirmPhoneChangeRequest
from src.core.shared.application.interfaces.cache_service import ICacheService


class ConfirmPhoneChangeUseCase:
    def __init__(
        self,
        uow: AbstractIAMUnitOfWork,
        otp_service: OTPService,
        cache_service: ICacheService,
    ):
        self.uow = uow
        self.otp_service = otp_service
        self.cache_service = cache_service

    async def execute(self, account_id: UUID, dto: ConfirmPhoneChangeRequest):
        pending_phone = await self.cache_service.get(f"phone_change:pending:{account_id}")
        if not pending_phone:
            raise ValueError("Запрос на смену номера телефона истёк или не найден")

        await self.otp_service.verify(
            account_id=account_id,
            otp_type=OTPType.CHANGE_PHONE,
            otp_value=dto.otp_code
        )

        async with self.uow as uow:
            account = await uow.account.get_account_by_id(account_id)
            if not account:
                raise ValueError("Account not found")

            account.change_phone(Phone(pending_phone))
            await uow.account.save(account)
            await uow.commit()

        await self.cache_service.delete(f"phone_change:pending:{account_id}")