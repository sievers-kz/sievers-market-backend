import pytest

from src.core.iam.presentation.dto import AccountConfirmation, LoginAccount, ForgotPasswordData
from src.core.iam.domain.enums import TokenType
from tests.iam.conftest import create_user_request, get_token_by_type


class TestForgotPasswordUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_forgot_password_request(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        forgot_password_usecase,
        account_repository,
        mock_notifier
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        email_token = get_token_by_type(user.tokens, TokenType.EMAIL)

        confirmation_dto = AccountConfirmation(confirm_token=email_token.value)
        await account_confirmation_usecase.execute(confirmation_dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        await forgot_password_usecase.execute(forgot_password_data)

        user_after_forgot_request = await account_repository.get_account_by_email(dto.email)
        password_token = get_token_by_type(user_after_forgot_request.tokens, TokenType.PASSWORD)

        assert password_token is not None
        assert password_token.is_expired() is False
        assert password_token.is_revoked is False
        assert password_token.type == TokenType.PASSWORD

        mock_notifier.send_password_recovery.assert_called_once()
        mock_notifier.send_password_recovery.assert_called_once_with(
            destination=dto.email,
            code=password_token.value
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_does_not_reveal_non_existent_email(self, forgot_password_usecase, mock_notifier):
        fake_data = ForgotPasswordData(email="nonexistent@example.com")
        await forgot_password_usecase.execute(fake_data)
        mock_notifier.send_password_recovery.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_revokes_old_tokens_on_multiple_forgot_password_requests(
        self,
        create_user_usecase,
        forgot_password_usecase,
        account_repository,
        mock_notifier
    ):
        dto = create_user_request()
        await create_user_usecase.execute(dto)

        forgot_password_data = ForgotPasswordData(email=dto.email)
        for iteration in range(3):
            await forgot_password_usecase.execute(forgot_password_data)

        user = await account_repository.get_account_by_email(dto.email)
        password_tokens = [token for token in user.tokens if token.type == TokenType.PASSWORD]

        assert len(password_tokens) == 3
        assert password_tokens[0].is_revoked is True
        assert password_tokens[1].is_revoked is True
        assert password_tokens[2].is_revoked is False
        assert mock_notifier.send_password_recovery.call_count == 3
