import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.users.application.usecases import EmailConfirmationUseCase
from src.core.users.domain.exceptions.exception_classes import InvalidEmailConfirmationCodeError


class TestEmailConfirmationUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None
        self.use_case = EmailConfirmationUseCase(unit_of_work=self.unit_of_work_mock)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_email_confirmation_success(self):
        """TEST: Successfully user email confirmation"""
        mock_identity = MagicMock(user_id=uuid.uuid4(), revoke_token=MagicMock())
        mock_user = MagicMock(confirm_user=MagicMock())

        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity
        self.unit_of_work_mock.user.get_user_by_id.return_value = mock_user

        confirmation_data = MagicMock(confirmation_code="email_confirmation_token")
        await self.use_case.execute(confirmation_data)

        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(confirmation_data.confirmation_code)
        self.unit_of_work_mock.user.get_user_by_id.assert_called_once_with(mock_identity.user_id)

        mock_user.confirm_user.assert_called_once()
        mock_identity.revoke_token.assert_called_once_with(confirmation_data.confirmation_code)

        self.unit_of_work_mock.user.save.assert_called_once_with(mock_user)
        self.unit_of_work_mock.identity.save.assert_called_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_email_confirmation_failed(self):
        """TEST: Failed user email confirmation"""
        self.unit_of_work_mock.identity.find_by_token_value.return_value = None
        confirmation_data = MagicMock(confirmation_code="invalid_token")

        with pytest.raises(InvalidEmailConfirmationCodeError):
            await self.use_case.execute(confirmation_data)

        self.unit_of_work_mock.user.save.assert_not_called()
        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()
