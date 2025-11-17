import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from src.core.auth.domain.entities import UserIdentity, UserCredentialsIdentity, UserTokenIdentity
from src.core.auth.domain.enums import TokenTypeEnum


class TestUserIdentityAggregate:
    @pytest.mark.unit
    def test_reset_password_and_revoke_all_sessions(self):
        mock_credentials = MagicMock()
        active_token_1 = MagicMock(token_type=TokenTypeEnum.REFRESH_TOKEN, is_revoked=False, revoke_token=MagicMock())
        active_token_2 = MagicMock(token_type=TokenTypeEnum.REFRESH_TOKEN, is_revoked=False, revoke_token=MagicMock())
        revoked_token_3 = MagicMock(token_type=TokenTypeEnum.REFRESH_TOKEN, is_revoked=True, revoke_token=MagicMock())

        mock_identity = UserIdentity(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            credentials=mock_credentials,
            tokens=[active_token_1, active_token_2, revoked_token_3]
        )

        mocked_new_password = "mocked_new_password"
        mock_identity.reset_password(mocked_new_password)
        mock_credentials.change_password.assert_called_once_with(mocked_new_password)

        active_token_1.revoke_token.assert_called_once()
        active_token_2.revoke_token.assert_called_once()
        revoked_token_3.revoke_token.assert_not_called()

    @pytest.mark.unit
    def test_revoke_token_success(self):
        active_token_mock = MagicMock(token_value="active_token_mock", is_revoked=False, revoke_token=MagicMock())
        mock_identity = UserIdentity(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            credentials=MagicMock(),
            tokens=[active_token_mock]
        )

        mock_identity.revoke_token("active_token_mock")
        active_token_mock.revoke_token.assert_called_once()

    @pytest.mark.unit
    def test_revoke_token_not_found(self):
        active_token_mock = MagicMock(token_value="real_token", revoke_token=MagicMock())
        mock_identity = UserIdentity(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            credentials=MagicMock(),
            tokens=[active_token_mock]
        )

        result = mock_identity.revoke_token("nonexistent_token")
        assert result is None
        active_token_mock.revoke_token.assert_not_called()


class TestUserCredentialsIdentity:
    @pytest.mark.unit
    @patch('src.core.auth.domain.value_objects.HashedPassword.from_raw')
    @patch('src.core.auth.domain.entities.datetime')
    def test_change_password_updates_hash_and_time(self, mock_datetime, mock_hashed_from_raw):
        old_time = datetime.utcnow() - timedelta(days=1)
        new_time = datetime.utcnow()

        mock_datetime.utcnow.return_value = new_time

        mock_old_hash = MagicMock(hashed_password="old_hash")
        mock_new_hash_vo = MagicMock(hashed_password="new_hash")
        mock_hashed_from_raw.return_value = mock_new_hash_vo

        credentials = UserCredentialsIdentity(
            id=uuid.uuid4(),
            auth_id=uuid.uuid4(),
            hashed_password=mock_old_hash,
            password_changed_at=old_time
        )

        NEW_PASSWORD = "new_raw_password"
        credentials.change_password(NEW_PASSWORD)

        mock_hashed_from_raw.assert_called_once_with(NEW_PASSWORD)

        assert credentials.hashed_password == mock_new_hash_vo
        assert credentials.password_changed_at == new_time
        assert credentials.password_changed_at > old_time


class TestUserTokenIdentity:
    @pytest.mark.unit
    @patch('src.core.auth.domain.entities.datetime')
    def test_token_is_expired_success(self, mock_datetime):
        expires_at_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        token = UserTokenIdentity.create(
            auth_id=uuid.uuid4(),
            token_type=TokenTypeEnum.ACCESS_TOKEN,
            token_value="test",
            expires_at=expires_at_time
        )

        mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 1, 0, tzinfo=timezone.utc)
        assert token.is_expired() is True

    @pytest.mark.unit
    @patch('src.core.auth.domain.entities.datetime')
    def test_token_is_not_expired_success(self, mock_datetime):
        expires_at_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        token = UserTokenIdentity.create(
            auth_id=uuid.uuid4(),
            token_type=TokenTypeEnum.ACCESS_TOKEN,
            token_value="test",
            expires_at=expires_at_time
        )

        mock_datetime.now.return_value = datetime(2025, 1, 1, 9, 59, 0, tzinfo=timezone.utc)
        assert token.is_expired() is False

    @pytest.mark.unit
    @patch('src.core.auth.domain.entities.datetime')
    def test_token_is_not_expired_at_exact_time(self, mock_datetime):
        expires_at_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        token = UserTokenIdentity.create(
            auth_id=uuid.uuid4(),
            token_type=TokenTypeEnum.ACCESS_TOKEN,
            token_value="test",
            expires_at=expires_at_time
        )

        mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        assert token.is_expired() is False