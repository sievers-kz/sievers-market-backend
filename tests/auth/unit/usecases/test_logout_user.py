import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.auth.application.usecases import LogoutUserUseCase
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError


class TestLogoutUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.token_service_mock = MagicMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = LogoutUserUseCase(unit_of_work=self.unit_of_work_mock, token_service=self.token_service_mock)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_logout_user_success(self):
        """[ TEST ]: Successfully user logout"""
        user_id_from_jwt = uuid.uuid4()
        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.REFRESH_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_jwt, revoke_token=MagicMock())
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        refresh_data = MagicMock(refresh_token="TEST_REFRESH_TOKEN")
        await self.use_case.execute(refresh_data)

        self.token_service_mock.verify_token.assert_called_once_with(
            refresh_data.refresh_token,
            TokenTypeEnum.REFRESH_TOKEN
        )

        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(
            refresh_data.refresh_token
        )

        mock_identity.revoke_token.assert_called_once_with(
            refresh_data.refresh_token
        )

        self.unit_of_work_mock.identity.save.assert_called_once_with(mock_identity)
        self.unit_of_work_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_logout_user_id_mismatch_fail(self):
        user_id_from_jwt = uuid.uuid4()
        user_id_from_db = uuid.uuid4()

        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.REFRESH_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_db)
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        refresh_data = MagicMock(refresh_token="WRONG_REFRESH_TOKEN")
        with pytest.raises(TokenStateError):
            await self.use_case.execute(refresh_data)

        self.token_service_mock.verify_token.assert_called_once_with(
            refresh_data.refresh_token,
            TokenTypeEnum.REFRESH_TOKEN
        )

        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(
            refresh_data.refresh_token
        )

        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()

