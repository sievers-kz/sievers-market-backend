import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.application.usecases import CreateUserUseCase


class TestCreateUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.email_sender = AsyncMock()
        self.token_service_mock = MagicMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = CreateUserUseCase(
            unit_of_work=self.unit_of_work_mock,
            email_sender=self.email_sender,
            token_service=self.token_service_mock
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    @patch(target="src.core.auth.application.usecases.registration.UserFactory")
    @patch(target="src.core.auth.application.usecases.registration.UserIdentityFactory")
    async def test_create_user_success(self, user_identity_factory_mock: MagicMock, user_factory_mock: MagicMock):
        mock_email = MagicMock(value="test@example.com")
        mock_user = MagicMock(id=uuid.uuid4(), email=mock_email)
        user_factory_mock.create.return_value = mock_user

        mock_identity = MagicMock()
        user_identity_factory_mock.create.return_value = mock_identity

        mock_token = MagicMock(token_value="TEST_TOKEN", token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)
        self.token_service_mock.create_auth_token.return_value = mock_token

        mock_user_data = MagicMock()
        mock_user_data.credentials = MagicMock()
        await self.use_case.execute(mock_user_data)

        user_factory_mock.create.assert_called_once_with(mock_user_data)
        self.unit_of_work_mock.user.save.assert_awaited_once_with(mock_user)

        self.token_service_mock.create_auth_token.assert_called_once_with(
            user_id=mock_user.id,
            token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN
        )

        user_identity_factory_mock.create.assert_called_once_with(
            user_id=mock_user.id,
            credentials=mock_user_data.credentials,
            tokens=[mock_token]
        )

        self.unit_of_work_mock.identity.save.assert_awaited_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_awaited_once()

        self.email_sender.send_email_confirmation.assert_awaited_once_with(
            to_email=mock_user.email.value,
            template_data={
                "confirmation_token": mock_token.token_value
            }
        )