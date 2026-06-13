import pytest

from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.exceptions import OTPCooldownError
from src.core.iam.presentation.dto import AccountConfirmation, ForgotPasswordData
from tests.iam.conftest import create_user_request


class TestForgotPasswordUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_forgot_password_request(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        forgot_password_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user.id}"
        )

        confirmation_dto = AccountConfirmation(
            account_id=user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        user_after_forgot_request = await account_repository.get_account_by_email(
            dto.email
        )
        reset_password_otp_code = await redis_service.get(
            f"otp:{OTPType.PASSWORD_RESET.value}:{user_after_forgot_request.id}"
        )

        assert reset_password_otp_code is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_does_not_reveal_non_existent_email(
        self, forgot_password_usecase, redis_service
    ):
        fake_data = ForgotPasswordData(email="nonexistent@example.com")
        await forgot_password_usecase.execute(fake_data)

        otp_code = await redis_service.get(f"otp:{OTPType.PASSWORD_RESET.value}:*")
        assert otp_code is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_revokes_old_tokens_on_multiple_forgot_password_requests(
        self,
        create_user_usecase,
        forgot_password_usecase,
        account_confirmation_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user.id}"
        )

        confirmation_dto = AccountConfirmation(
            account_id=user.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        with pytest.raises(OTPCooldownError):
            await forgot_password_usecase.execute(forgot_password_data)
