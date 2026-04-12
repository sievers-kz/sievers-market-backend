import pytest

from src.api.iam.dto import ForgotPasswordData, ResetPasswordData, AccountConfirmation, LoginAccount
from src.core.iam.domain.enums import TokenType
from tests.iam.conftest import create_user_request, get_token_by_type


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
        mock_notifier
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user_after_registration = await account_repository.get_account_by_email(dto.email)
        email_token = get_token_by_type(user_after_registration.tokens, TokenType.EMAIL)

        confirmation_dto = AccountConfirmation(confirm_token=email_token.value)
        await account_confirmation_usecase.execute(confirmation_dto)

        login_dto = LoginAccount(email=dto.email, raw_password=dto.raw_password)
        await login_user_usecase.execute(login_dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        user = await account_repository.get_account_by_email(dto.email)
        password_token = get_token_by_type(user.tokens, TokenType.PASSWORD)

        reset_password_data = ResetPasswordData(raw_password="super_secret", password_reset_token=password_token.value)
        await reset_password_usecase.execute(reset_password_data)

        user_after_reset_password = await account_repository.get_account_by_email(dto.email)
        password_token = get_token_by_type(user_after_reset_password.tokens, TokenType.PASSWORD)
        refresh_tokens = [token for token in user_after_reset_password.tokens if token.type == TokenType.REFRESH]

        assert password_token.is_revoked is True
        for token in refresh_tokens:
            assert token.is_revoked is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_on_reused_password_token(
        self,
        create_user_usecase,
        forgot_password_usecase,
        reset_password_usecase,
        account_repository,
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        user = await account_repository.get_account_by_email(dto.email)
        password_token = get_token_by_type(user.tokens, TokenType.PASSWORD)

        reset_password_data = ResetPasswordData(raw_password="super_secret", password_reset_token=password_token.value)
        await reset_password_usecase.execute(reset_password_data)

        with pytest.raises(Exception) as exc:
            await reset_password_usecase.execute(reset_password_data)

        assert str(exc.value) == "Token is already revoked"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_fails_with_wrong_token(self, reset_password_usecase):
        reset_password_data = ResetPasswordData(raw_password="supersecret", password_reset_token="wrong_password_token")
        with pytest.raises(Exception) as exc:
            await reset_password_usecase.execute(reset_password_data)
        assert str(exc.value) == "Invalid reset password token"
