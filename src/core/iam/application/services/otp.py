import secrets
from uuid import UUID

from loguru import logger

from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import InvalidOTPCodeError, OTPCooldownError
from src.core.shared.application.interfaces.cache_service import ICacheService
from src.core.shared.application.interfaces.queue_service import IQueueService
from src.core.shared.infrastructure.tasks import TaskNames


class OTPService:
    TASK_OTP_MAP = {
        OTPType.CONFIRMATION: TaskNames.SEND_OTP_EMAIL,
        OTPType.PASSWORD_RESET: TaskNames.SEND_OTP_PASSWORD_RESET,
        OTPType.CHANGE_EMAIL: TaskNames.SEND_OTP_CHANGE_EMAIL,
        OTPType.CHANGE_PHONE: TaskNames.SEND_OTP_CHANGE_PHONE,
    }

    def __init__(self, cache: ICacheService, queue: IQueueService):
        self.cache = cache
        self.queue = queue

    async def send(self, account_id: UUID, email: str, otp_type: OTPType) -> None:
        cooldown_key = f"otp:cooldown:{otp_type.value}:{account_id}"
        if await self.cache.get(cooldown_key) is not None:
            logger.warning(
                "OTP COOLDOWN ACTIVE | account_id={} otp_type={}", account_id, otp_type
            )
            raise OTPCooldownError()

        otp_code = "".join(secrets.choice("0123456789") for _ in range(6))
        await self.cache.set(
            key=f"otp:{otp_type.value}:{account_id}", value=otp_code, ttl=300
        )
        await self.cache.set(key=cooldown_key, value="1", ttl=60)

        await self.queue.enqueue(
            task_name=self.TASK_OTP_MAP[otp_type],
            to=email,
            code=otp_code,
        )
        logger.info("OTP SENT | account_id={} otp_type={}", account_id, otp_type)

    async def verify(self, account_id: UUID, otp_type: OTPType, otp_value: int) -> bool:
        cached_otp = await self.cache.get(key=f"otp:{otp_type.value}:{account_id}")
        if not cached_otp or cached_otp != otp_value:
            logger.warning(
                "OTP VERIFICATION FAILED | account_id={} otp_type={}",
                account_id,
                otp_type,
            )
            raise InvalidOTPCodeError()

        logger.info("OTP VERIFIED | account_id={} otp_type={}", account_id, otp_type)
        await self.cache.delete(f"otp:{otp_type.value}:{account_id}")
