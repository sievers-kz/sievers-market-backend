from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from src.core.iam.domain.enums import TokenType
from src.core.iam.domain.value_objects import Password
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher
from tests.iam.conftest import create_domain_account, get_token_by_type, get_token_by_value


@pytest.mark.unit
def test_confirm_account_success():
    account = create_domain_account(is_active=False)
    token_value = "secret_confirm_token"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.EMAIL, token_value, expires_at)
    account.confirm_account(token_value)
    assert account.is_active is True


@pytest.mark.unit
def test_confirm_account_fails_when_token_not_found():
    account = create_domain_account(is_active=False)
    with pytest.raises(ValueError, match="Confirmation token not found"):
        account.confirm_account(token_value="non_existent_token")


@pytest.mark.unit
def test_confirm_account_fails_when_token_expired():
    account = create_domain_account(is_active=False)
    token_value = "secret_confirm_token"
    expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    account.add_new_token(TokenType.EMAIL, token_value, expires_at)

    with pytest.raises(ValueError, match="Confirmation token is expired"):
        account.confirm_account(token_value)


@pytest.mark.unit
def test_confirm_account_fails_when_already_active():
    account = create_domain_account(is_active=True)
    with pytest.raises(ValueError, match="Account is already confirmed"):
        account.confirm_account(token_value="secret_confirm_token")


@pytest.mark.unit
def test_login_success():
    account = create_domain_account(is_active=True)
    account.password = Password(value="hashed_password")

    mock_hasher = MagicMock(spec=AbstractPasswordHasher)
    mock_hasher.verify_password.return_value = True

    account.login("my_correct_password", mock_hasher)
    mock_hasher.verify_password.assert_called_once()


@pytest.mark.unit
def test_login_fails_when_user_inactive():
    account = create_domain_account(is_active=False)
    mock_hasher = MagicMock(spec=AbstractPasswordHasher)
    with pytest.raises(ValueError, match="Account is not confirmed"):
        account.login("my_incorrect_password", mock_hasher)


@pytest.mark.unit
def test_login_fails_with_invalid_credentials():
    account = create_domain_account(is_active=True)
    account.password = Password(value="current_password")

    mock_hasher = MagicMock(spec=AbstractPasswordHasher)
    mock_hasher.verify_password.return_value = False

    with pytest.raises(ValueError, match="Invalid email or password"):
        account.login("invalid_password", mock_hasher)


@pytest.mark.unit
def test_change_password_success():
    account = create_domain_account(is_active=True)
    account.password = Password(value="old_hashed_password")

    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.REFRESH, "refresh_token_123", expires_at)

    mock_hasher = MagicMock(spec=AbstractPasswordHasher)
    mock_hasher.verify_password.return_value = True

    account.change_password(
        "my_old_raw_password",
        "new_hashed_password",
        mock_hasher
    )
    assert account.password.value == "new_hashed_password"

    refresh_token = get_token_by_type(account.tokens, TokenType.REFRESH)
    assert refresh_token.is_revoked is True
    mock_hasher.verify_password.assert_called_once()


@pytest.mark.unit
def test_change_password_fails_with_wrong_old_password():
    account = create_domain_account(is_active=True)
    account.password = Password(value="old_hashed_password")

    mock_hasher = MagicMock(spec=AbstractPasswordHasher)
    mock_hasher.verify_password.return_value = False

    with pytest.raises(ValueError, match="Invalid password"):
        account.change_password(
            "wrong_old_password",
            "new_hashed_password",
            mock_hasher
        )


@pytest.mark.unit
def test_logout_success():
    account = create_domain_account(is_active=True)
    token_value = "valid_access_token"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.ACCESS, token_value, expires_at)

    account.logout(token_value)

    token = get_token_by_value(account.tokens, token_value)
    assert token.is_revoked is True


@pytest.mark.unit
def test_rotate_refresh_token_success():
    account = create_domain_account(is_active=True)
    old_token_value = "old_refresh_token"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.REFRESH, old_token_value, expires_at)

    new_token_value = "new_refresh_token"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.rotate_refresh_token(old_token_value, new_token_value, expires_at)

    old_refresh_token = get_token_by_value(account.tokens, old_token_value)
    new_refresh_token = get_token_by_value(account.tokens, new_token_value)

    assert old_refresh_token.is_revoked is True
    assert new_refresh_token.is_revoked is False


@pytest.mark.unit
def test_reset_password_success():
    account = create_domain_account(is_active=True)

    fake_refresh_token = "refresh_token_1"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.REFRESH, fake_refresh_token, expires_at)

    reset_password_token = "reset_password_token"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    account.add_new_token(TokenType.PASSWORD, reset_password_token, expires_at)
    new_hashed_password = "new_hashed_password"

    account.reset_password(reset_password_token, new_hashed_password)
    revoked_password_token = get_token_by_value(account.tokens, reset_password_token)
    assert revoked_password_token.is_revoked is True

    revoked_refresh_tokens = [token for token in account.tokens if token.type == TokenType.REFRESH]
    for token in revoked_refresh_tokens:
        assert token.is_revoked is True

