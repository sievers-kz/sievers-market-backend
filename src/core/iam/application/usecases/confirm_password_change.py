from uuid import UUID

from loguru import logger

from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import PasswordChangeRequestNotFoundError
from src.core.iam.domain.value_objects import HashedPassword
from src.core.iam.infrastructure.uow import IAMUnitOfWork
from src.core.iam.presentation.dto import ConfirmPasswordChange
from src.core.shared.infrastructure.services.redis_service import RedisService


class ConfirmPasswordChangeUseCase:
    def __init__(
        self,
        uow: IAMUnitOfWork,
        otp_service: OTPService,
        cache_service: RedisService,
    ):
        self.uow = uow
        self.otp_service = otp_service
        self.cache_service = cache_service

    async def execute(self, account_id: UUID, dto: ConfirmPasswordChange):
        pending_password = await self.cache_service.get(f"password_change:pending:{account_id}")
        if not pending_password:
            raise PasswordChangeRequestNotFoundError()

        await self.otp_service.verify(account_id=account_id, otp_type=OTPType.CHANGE_PASSWORD, otp_value=dto.otp_code)

        async with self.uow as uow:
            account = await uow.account.get_account_by_id(account_id)
            account.change_password(HashedPassword(pending_password))

            await uow.account.save(account)
            await uow.commit()

        await self.cache_service.delete(f"password_change:pending:{account_id}")
        logger.info("Password changed | account_id={}", account_id)
