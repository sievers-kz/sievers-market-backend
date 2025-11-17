import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.auth.application.usecases import ForgotPasswordUseCase
from src.core.auth.domain.enums import TokenTypeEnum


class TestForgotPasswordUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.token_service_mock = MagicMock()
        self.email_sender_mock = AsyncMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = ForgotPasswordUseCase(
            unit_of_work=self.unit_of_work_mock,
            token_service=self.token_service_mock,
            email_sender=self.email_sender_mock
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_forgot_password_success(self):
        mock_user = MagicMock(id=uuid.uuid4(), email="test@example.com")
        self.unit_of_work_mock.user.get_by_user_email.return_value = mock_user

        mock_token = MagicMock(
            token_type=TokenTypeEnum.PASSWORD_RESET_TOKEN,
            token_value="TEST_PASSWORD_RESET_TOKEN",
            expires_at=MagicMock()
        )
        self.token_service_mock.create_auth_token.return_value = mock_token

        mock_identity = MagicMock(user_id=mock_user.id, add_new_token=MagicMock())
        self.unit_of_work_mock.identity.get_user_identity.return_value = mock_identity

        forgot_password_data = MagicMock(email="test@example.com")
        await self.use_case.execute(forgot_password_data)

        self.unit_of_work_mock.user.get_by_user_email.assert_called_once_with(
            forgot_password_data.email
        )

        self.token_service_mock.create_auth_token.assert_called_once_with(
            mock_user.id,
            TokenTypeEnum.PASSWORD_RESET_TOKEN
        )

        self.unit_of_work_mock.identity.get_user_identity.assert_called_once_with(
            mock_user.id
        )

        mock_identity.add_new_token.assert_called_once_with(
            token_type=mock_token.token_type,
            token_value=mock_token.token_value,
            expires_at=mock_token.expires_at
        )

        self.unit_of_work_mock.identity.save.assert_called_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_called_once()

        self.email_sender_mock.send_password_reset_confirmation.assert_called_once_with(
            to_email=mock_user.email,
            template_data={
                "reset_password_token": mock_token.token_value
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_forgot_password_user_not_found(self):
        self.unit_of_work_mock.user.get_by_user_email.return_value = None
        forgot_password_data = MagicMock(email="nonexistent@example.com")

        with patch("asyncio.sleep", new=AsyncMock()) as sleep_mock:
            await self.use_case.execute(forgot_password_data)

        self.unit_of_work_mock.user.get_by_user_email.assert_called_once_with(
            forgot_password_data.email
        )

        sleep_mock.assert_called_once_with(0.5)

        self.token_service_mock.create_auth_token.assert_not_called()
        self.unit_of_work_mock.identity.assert_not_called()

        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()

        self.email_sender_mock.send_password_reset_confirmation.assert_not_called()
