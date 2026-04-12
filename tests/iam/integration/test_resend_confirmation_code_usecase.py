import pytest

from src.api.iam.dto import CreateUserRequest, AccountConfirmation, ResendCodeRequest
from tests.iam.conftest import mock_notifier


class TestResendConfirmationCodeUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_resend_confirmation_code(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        account_repository,
        resend_confirmation_code_usecase,
        mock_notifier
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        mock_notifier.send_confirmation_code.reset_mock()

        resend_dto = ResendCodeRequest(email=dto.email)
        await resend_confirmation_code_usecase.execute(resend_dto)

        user = await account_repository.get_account_by_email(dto.email)
        assert len(user.tokens) == 2

        old_token = user.tokens[0]
        new_token = user.tokens[1]

        assert old_token.is_revoked is True
        assert new_token.is_revoked is False

        mock_notifier.send_confirmation_code.assert_called_once_with(
            destination=dto.email,
            code=new_token.value
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_resend_fails_if_already_confirmed(
        self,
        create_user_usecase,
        account_confirmation_usecase,
        resend_confirmation_code_usecase,
        account_repository,
        mock_notifier
    ):
        dto = CreateUserRequest(
            email="test@example.com",
            raw_password="super_secret",
            last_name="Test",
            first_name="Test",
        )
        await create_user_usecase.execute(dto)

        user = await account_repository.get_account_by_email(dto.email)
        token_value = user.tokens[0].value

        confirmation_dto = AccountConfirmation(confirm_token=token_value)
        await account_confirmation_usecase.execute(confirmation_dto)

        mock_notifier.send_confirmation_code.reset_mock()
        resend_dto = ResendCodeRequest(email=dto.email)

        with pytest.raises(Exception):
            await resend_confirmation_code_usecase.execute(resend_dto)

        confirmed_user = await account_repository.get_account_by_email(dto.email)
        assert len(confirmed_user.tokens) == 1
        mock_notifier.send_confirmation_code.assert_not_called()
