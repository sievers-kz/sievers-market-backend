import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.auth.application.usecases import RefreshTokenUseCase
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.domain.exceptions.exception_classes import TokenStateError


class TestRefreshTokenUseCase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.unit_of_work_mock = AsyncMock()
        self.token_service_mock = MagicMock()

        self.unit_of_work_mock.__aenter__.return_value = self.unit_of_work_mock
        self.unit_of_work_mock.__aexit__.return_value = None

        self.use_case = RefreshTokenUseCase(unit_of_work=self.unit_of_work_mock, token_service=self.token_service_mock)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_refresh_token_success(self):
        user_id_from_jwt = uuid.uuid4()
        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.REFRESH_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_jwt, revoke_token=MagicMock(), add_new_token=MagicMock())
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        mock_access_token = MagicMock(
            token_type=TokenTypeEnum.ACCESS_TOKEN,
            token_value="TEST_NEW_ACCESS_TOKEN",
            expires_at=MagicMock()
        )
        mock_refresh_token = MagicMock(
            token_type=TokenTypeEnum.REFRESH_TOKEN,
            token_value="TEST_NEW_REFRESH_TOKEN",
            expires_at=MagicMock()
        )
        self.token_service_mock.create_auth_token.side_effect = [mock_access_token, mock_refresh_token]

        refresh_token_data = MagicMock(refresh_token="TEST_OLD_REFRESH_TOKEN")
        response = await self.use_case.execute(refresh_token_data)
        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(refresh_token_data.refresh_token)

        self.token_service_mock.create_auth_token.assert_any_call(
            user_id=user_id_from_jwt,
            token_type=TokenTypeEnum.ACCESS_TOKEN
        )
        self.token_service_mock.create_auth_token.assert_any_call(
            user_id=user_id_from_jwt,
            token_type=TokenTypeEnum.REFRESH_TOKEN
        )
        assert self.token_service_mock.create_auth_token.call_count == 2

        mock_identity.revoke_token.assert_called_once_with(refresh_token_data.refresh_token)
        mock_identity.add_new_token.assert_called_once_with(
            token_type=mock_refresh_token.token_type,
            token_value=mock_refresh_token.token_value,
            expires_at=mock_refresh_token.expires_at
        )

        assert self.unit_of_work_mock.identity.save.call_count == 2
        self.unit_of_work_mock.commit.assert_called_once()

        assert response.access_token == "TEST_NEW_ACCESS_TOKEN"
        assert response.refresh_token == "TEST_NEW_REFRESH_TOKEN"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_refresh_token_id_mismatch_fail(self):
        user_id_from_jwt = uuid.uuid4()
        user_id_from_db = uuid.uuid4()

        mock_payload = {"sub": str(user_id_from_jwt), "token_type": TokenTypeEnum.REFRESH_TOKEN}
        self.token_service_mock.verify_token.return_value = mock_payload

        mock_identity = MagicMock(user_id=user_id_from_db)
        self.unit_of_work_mock.identity.find_by_token_value.return_value = mock_identity

        refresh_token_data = MagicMock(refresh_token="WRONG_REFRESH_TOKEN")
        with pytest.raises(TokenStateError):
            await self.use_case.execute(refresh_token_data)

        self.token_service_mock.verify_token.assert_called_once_with(
            refresh_token_data.refresh_token,
            TokenTypeEnum.REFRESH_TOKEN
        )

        self.unit_of_work_mock.identity.find_by_token_value.assert_called_once_with(
            refresh_token_data.refresh_token
        )

        self.unit_of_work_mock.identity.save.assert_not_called()
        self.unit_of_work_mock.commit.assert_not_called()
