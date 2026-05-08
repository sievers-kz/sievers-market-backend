from uuid import UUID

from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.value_objects import Phone
from src.core.iam.presentation.dto import ChangePhoneRequest
from src.core.shared.application.interfaces.cache_service import ICacheService
from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer


class RequestPhoneChangeUseCase:
    def __init__(
        self,
        uow: AbstractIAMUnitOfWork,
        otp_service: OTPService,
        cache_service: ICacheService,
    ):
        self.uow = uow
        self.otp_service = otp_service
        self.cache_service = cache_service

    async def execute(self, account_id: UUID, dto: ChangePhoneRequest):
        normalized_phone = PhoneNormalizer().normalize(dto.phone)
        phone_vo = Phone(normalized_phone)

        async with self.uow as uow:
            account = await uow.account.get_account_by_id(account_id)
            if not account:
                raise ValueError("Account not found")

            await self.cache_service.set(
                key=f"phone_change:pending:{account_id}",
                value=phone_vo.value,
                ttl=300
            )

            await self.otp_service.send(
                account_id=account_id,
                email=account.email.value,
                otp_type=OTPType.CHANGE_PHONE
            )
