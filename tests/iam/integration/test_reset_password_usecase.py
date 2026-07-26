import pytest

from src.core.iam.domain.enums import OTPType, TokenType
from src.core.iam.domain.exceptions import InvalidOTPCodeError
from src.core.iam.presentation.dto import (
    AccountConfirmation,
    ForgotPasswordData,
    LoginAccount,
    ResetPasswordData,
)
from tests.iam.conftest import create_user_request


class TestResetPasswordUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_reset_password(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        login_user_usecase,
        forgot_password_usecase,
        reset_password_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user_after_registration = await account_repository.get_account_by_email(
            dto.email
        )
        otp_code = await redis_service.get(
            f"otp:{OTPType.CONFIRMATION.value}:{user_after_registration.id}"
        )

        confirmation_dto = AccountConfirmation(
            account_id=user_after_registration.id, confirm_code=otp_code
        )
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        user = await account_repository.get_account_by_email(dto.email)
        password_reset_otp_code = await redis_service.get(
            f"otp:{OTPType.PASSWORD_RESET.value}:{user.id}"
        )

        reset_password_data = ResetPasswordData(
            email=dto.email,
            raw_password="supersecret",
            password_reset_otp=password_reset_otp_code,
        )
        await reset_password_usecase.execute(reset_password_data)

        otp_after_reset = await redis_service.get(
            f"otp:{OTPType.PASSWORD_RESET.value}:{user.id}"
        )
        assert otp_after_reset is None

        user_after_reset_password = await account_repository.get_account_by_email(
            dto.email
        )
        refresh_tokens = [
            token
            for token in user_after_reset_password.tokens
            if token.type == TokenType.REFRESH
        ]

        for token in refresh_tokens:
            assert token.is_revoked is True

        login_dto = LoginAccount(email=dto.email, raw_password="supersecret")
        response = await login_user_usecase.execute(login_dto)
        assert response.access_token is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_on_reused_otp(
        self,
        create_user_usecase,
        forgot_password_usecase,
        reset_password_usecase,
        account_repository,
        redis_service,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        otp_code = await redis_service.get(
            f"otp:{OTPType.PASSWORD_RESET.value}:{user.id}"
        )
        reset_password_data = ResetPasswordData(
            email=dto.email, raw_password="supersecret", password_reset_otp=otp_code
        )
        await reset_password_usecase.execute(reset_password_data)

        with pytest.raises(InvalidOTPCodeError):
            await reset_password_usecase.execute(reset_password_data)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_otp(
        self,
        create_user_usecase,
        reset_password_usecase,
        account_repository,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        reset_password_data = ResetPasswordData(
            email=dto.email, raw_password="supersecret", password_reset_otp="000000"
        )
        with pytest.raises(InvalidOTPCodeError):
            await reset_password_usecase.execute(reset_password_data)
