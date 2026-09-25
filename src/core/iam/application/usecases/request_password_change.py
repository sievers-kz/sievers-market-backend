from uuid import UUID

from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import PasswordMismatchError
from src.core.iam.infrastructure.services.password_service import PasswordService
from src.core.iam.infrastructure.uow import IAMUnitOfWork
from src.core.iam.presentation.dto import RequestPasswordChange
from src.core.shared.infrastructure.services.redis_service import RedisService


class RequestPasswordChangeUseCase:
    def __init__(
        self,
        uow: IAMUnitOfWork,
        password_service: PasswordService,
        otp_service: OTPService,
        cache_service: RedisService,
    ):
        self.uow = uow
        self.password_service = password_service
        self.otp_service = otp_service
        self.cache_service = cache_service

    async def execute(self, account_id: UUID, dto: RequestPasswordChange):
        async with self.uow as uow:
            account = await uow.account.get_account_by_id(account_id)

            validated_plain = self.password_service.validate(dto.new_password)
            if not self.password_service.verify(dto.raw_password, account.password.value):
                raise PasswordMismatchError()

            new_hashed_password = self.password_service.hash(validated_plain)
            await self.cache_service.set(
                key=f"password_change:pending:{account_id}", value=new_hashed_password.value, ttl=300
            )
            await self.otp_service.send(
                account_id=account_id, email=account.email.value, otp_type=OTPType.CHANGE_PASSWORD
            )
