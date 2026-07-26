import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import OTPCooldownError
from src.core.iam.presentation.dto import CreateAccountRequest, ResendCodeRequest
from tests.iam.conftest import create_user_request


class TestResendConfirmationCodeUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_resend_confirmation_code(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        account_repository,
        resend_confirmation_code_usecase,
        redis_service,
    ):
        dto = CreateAccountRequest(
            email="test@example.com",
            raw_password="super_secret",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        await redis_service.delete(
            f"otp:cooldown:{OTPType.CONFIRMATION.value}:{user.id}"
        )

        resend_dto = ResendCodeRequest(email=dto.email)
        await resend_confirmation_code_usecase.execute(resend_dto)

        new_otp = await redis_service.get(f"otp:{OTPType.CONFIRMATION.value}:{user.id}")
        assert new_otp is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_cooldown_blocks_immediate_resend(
        self,
        create_user_usecase,
        resend_confirmation_code_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        resend_dto = ResendCodeRequest(email=dto.email)
        with pytest.raises(OTPCooldownError):
            await resend_confirmation_code_usecase.execute(resend_dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_silent_on_nonexistent_email(
        self,
        resend_confirmation_code_usecase,
        account_repository,
    ):
        resend_dto = ResendCodeRequest(email="ghost@example.com")
        await resend_confirmation_code_usecase.execute(resend_dto)
