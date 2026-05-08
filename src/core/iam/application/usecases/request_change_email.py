from uuid import UUID

from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.value_objects import Email
from src.core.iam.presentation.dto import ChangeEmailRequest
from src.core.shared.application.interfaces.cache_service import ICacheService


class RequestEmailChangeUseCase:
    def __init__(
        self,
        uow: AbstractIAMUnitOfWork,
        otp_service: OTPService,
        cache_service: ICacheService
    ):
        self.uow = uow
        self.otp_service = otp_service
        self.cache_service = cache_service

    async def execute(self, account_id: UUID, dto: ChangeEmailRequest):
        email_vo = Email(dto.email)
        async with self.uow as uow:
            account = await uow.account.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found!")

            existing = await uow.account.get_account_by_email(email_vo.value)
            if existing:
                raise ValueError("Email already exists!")

        await self.cache_service.set(
            key=f"email_change:pending:{account_id}",
            value=email_vo.value,
            ttl=300
        )

        await self.otp_service.send(
            account_id=account_id,
            email=email_vo.value,
            otp_type=OTPType.CHANGE_EMAIL
        )

