import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError
from src.core.users.application.usecases import ResetPasswordUseCase


class TestResetPasswordUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.token_service_mock = MagicMock()
        self.password_hasher_mock = MagicMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = ResetPasswordUseCase(
            unit_of_work=self.unit_of_work_mock,
            token_service=self.token_service_mock,
            password_hasher=self.password_hasher_mock
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_reset_password_success(self):
        user_id_from_jwt = uuid.uuid4()

        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.PASSWORD_RESET_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_jwt, reset_password=MagicMock())
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        mock_new_hashed_password = "new_hashed_password"
        self.password_hasher_mock.hash_password.return_value = mock_new_hashed_password

        reset_password_data = MagicMock(reset_password_token="reset_password_token", new_password="new_password123")
        await self.use_case.execute(reset_password_data)

        self.token_service_mock.verify_token.assert_called_once_with(
            reset_password_data.reset_password_token,
            TokenTypeEnum.PASSWORD_RESET_TOKEN
        )

        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(
            reset_password_data.reset_password_token
        )

        self.password_hasher_mock.hash_password.assert_called_once_with(reset_password_data.new_password)
        mock_identity.reset_password.assert_called_once_with(mock_new_hashed_password)

        self.unit_of_work_mock.identity.save.assert_called_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_reset_password_id_mismatch_fail(self):
        user_id_from_jwt = uuid.uuid4()
        user_id_from_db = uuid.uuid4()

        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.PASSWORD_RESET_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_db)
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        reset_password_data = MagicMock(reset_password_token="reset_password_token", new_password="new_password123")

        with pytest.raises(TokenStateError):
            await self.use_case.execute(reset_password_data)

        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()


