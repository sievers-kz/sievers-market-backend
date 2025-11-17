import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.auth.application.usecases import LoginUserUseCase
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import InvalidCredentialsError


class TestLoginUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.token_service_mock = MagicMock()
        self.password_hasher = MagicMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = LoginUserUseCase(
            unit_of_work=self.unit_of_work_mock,
            token_service=self.token_service_mock,
            password_hasher=self.password_hasher
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_login_user_success(self):
        mock_user = MagicMock(id=uuid.uuid4())
        self.unit_of_work_mock.user.get_by_user_email.return_value = mock_user

        mock_identity = MagicMock(user_id=mock_user.id, credentials=MagicMock(), add_new_token=MagicMock())
        self.unit_of_work_mock.identity.get_user_identity.return_value = mock_identity

        mock_password_hasher_result = True
        self.password_hasher.verify_password.return_value = mock_password_hasher_result

        mock_access_token = MagicMock(
            token_type=TokenTypeEnum.ACCESS_TOKEN,
            token_value="TEST_ACCESS_TOKEN",
            expires_at=MagicMock()
        )
        mock_refresh_token = MagicMock(
            token_type=TokenTypeEnum.REFRESH_TOKEN,
            token_value="TEST_REFRESH_TOKEN",
            expires_at=MagicMock()
        )

        self.token_service_mock.create_auth_token.side_effect = [mock_access_token, mock_refresh_token]

        login_data = MagicMock(email="test@example.com", raw_password="password123")
        response = await self.use_case.execute(login_data)

        self.unit_of_work_mock.user.get_by_user_email.assert_called_once_with(login_data.email)
        self.unit_of_work_mock.identity.get_user_identity.assert_called_once_with(mock_user.id)

        self.password_hasher.verify_password.assert_called_once_with(
            login_data.raw_password,
            mock_identity.credentials.hashed_password.hashed_password
        )

        mock_identity.add_new_token.assert_called_once_with(
            token_type=mock_refresh_token.token_type,
            token_value=mock_refresh_token.token_value,
            expires_at=mock_refresh_token.expires_at
        )

        self.unit_of_work_mock.identity.save.assert_called_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_called_once()

        assert response.access_token == "TEST_ACCESS_TOKEN"
        assert response.refresh_token == "TEST_REFRESH_TOKEN"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_login_user_invalid_email(self):
        self.unit_of_work_mock.user.get_by_user_email.return_value = None
        login_data = MagicMock(email="nonexistent@example.com", raw_password="password123")

        with pytest.raises(InvalidCredentialsError):
            await self.use_case.execute(login_data)

        self.unit_of_work_mock.user.get_by_user_email.assert_called_once_with(login_data.email)
        self.unit_of_work_mock.identity.get_user_identity.assert_not_called()
        self.token_service_mock.create_auth_token.assert_not_called()

        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_login_user_password_mismatch(self):
        mock_user = MagicMock(id=uuid.uuid4())
        self.unit_of_work_mock.user.get_by_user_email.return_value = mock_user

        mock_identity = MagicMock(user_id=mock_user.id, credentials=MagicMock())
        self.unit_of_work_mock.identity.get_user_identity.return_value = mock_identity

        mock_password_hasher_result = False
        self.password_hasher.verify_password.return_value = mock_password_hasher_result

        login_data = MagicMock(email="test@example.com", raw_password="wrong_password")
        with pytest.raises(InvalidCredentialsError):
            await self.use_case.execute(login_data)

        self.unit_of_work_mock.user.get_by_user_email.assert_called_once_with(login_data.email)
        self.unit_of_work_mock.identity.get_user_identity.assert_called_once_with(mock_user.id)

        self.password_hasher.verify_password.assert_called_once_with(
            login_data.raw_password,
            mock_identity.credentials.hashed_password.hashed_password
        )

        self.token_service_mock.create_auth_token.assert_not_called()
        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()
