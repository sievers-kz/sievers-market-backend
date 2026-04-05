from datetime import timezone, datetime, timedelta

import pytest

from src.core.iam.domain.entities import Account
from src.core.iam.domain.enums import TokenType
from tests.iam.conftest import create_domain_account


class TestAccountRepository:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_repository_saves_and_retrieves_account(self, account_repository):
        domain_account = create_domain_account(is_active=True)
        await account_repository.save(domain_account)
        saved_account = await account_repository.get_account_by_id(domain_account.id)

        assert saved_account is not None
        assert isinstance(saved_account, Account)
        assert saved_account.id == domain_account.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_find_by_token_value_success(self, account_repository):
        domain_account = create_domain_account(is_active=True)
        token_value = "fake_token_value"
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        domain_account.add_new_token(TokenType.REFRESH, token_value, expires_at)

        await account_repository.save(domain_account)
        found_account = await account_repository.find_by_token_value(token_value)

        assert found_account is not None
        assert found_account.id == domain_account.id

        assert len(found_account.tokens) > 0
        assert any(t.value == token_value for t in found_account.tokens)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_find_by_token_value_returns_none_for_invalid_token(self, account_repository):
        fake_token = "fake_token_value"
        found_account = await account_repository.find_by_token_value(fake_token)
        assert found_account is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_existing_account_merge(self, account_repository):
        domain_account = create_domain_account(is_active=True)
        await account_repository.save(domain_account)

        token_value = "fake_token_value"
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        domain_account.add_new_token(TokenType.REFRESH, token_value, expires_at)

        account_id = domain_account.id
        domain_account.is_active = False

        domain_account.add_new_token(
            type=TokenType.REFRESH,
            value="merged_refresh_token_123",
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        await account_repository.save(domain_account)

        updated_account = await account_repository.get_account_by_id(account_id)

        assert updated_account.is_active is False
        assert len(updated_account.tokens) == 2
        assert any(t.value == "merged_refresh_token_123" for t in updated_account.tokens)