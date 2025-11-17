import uuid

import pytest

from src.api.auth.auth_dto import UserCredentialsDTO
from src.core.auth.domain.entities import UserIdentity as DomainUserIdentity
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.auth_repository import UserIdentityRepository
from src.core.users.infrastructure.user_repository import UserRepository


class TestUserIdentityRepository:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, database_session, create_domain_user_from_dto, create_domain_user_identity_from_dto):
        self.user_repository = UserRepository(database_session)
        self.user_identity_repository = UserIdentityRepository(database_session)
        self.create_user = create_domain_user_from_dto
        self.create_user_identity = create_domain_user_identity_from_dto
        self.session = database_session

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_identity_success(self):
        user = self.create_user(email="test.create.user.for.identity@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        identity = self.create_user_identity(user.id)
        await self.user_identity_repository.save(identity)
        await self.session.commit()

        saved_identity = await self.user_identity_repository.get_user_identity(user.id)
        assert isinstance(saved_identity, DomainUserIdentity)
        assert saved_identity is not None
        assert saved_identity.user_id == user.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_identity_not_found(self):
        user_id = uuid.uuid4()
        identity = await self.user_identity_repository.get_user_identity(user_id)
        assert identity is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_find_by_token_value_success(self):
        user = self.create_user(email="test.create.user.for.identity.token@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        identity = self.create_user_identity(user.id)
        await self.user_identity_repository.save(identity)
        await self.session.commit()

        email_token = identity.get_current_token(TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN)
        saved_identity = await self.user_identity_repository.find_by_token_value(email_token.token_value)
        assert saved_identity is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_find_by_token_value_not_found(self):
        user = self.create_user(email="test.find.nonexistent.token.value@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        identity = self.create_user_identity(user.id)
        await self.user_identity_repository.save(identity)
        await self.session.commit()

        email_token = "WRONG_TOKEN"
        saved_identity = await self.user_identity_repository.find_by_token_value(email_token)
        assert saved_identity is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_updated_user_password(self):
        user = self.create_user(email="test.save.updated.user.password@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        identity = self.create_user_identity(user.id)
        await self.user_identity_repository.save(identity)
        await self.session.commit()

        original_identity = await self.user_identity_repository.get_user_identity(user.id)
        original_hash = original_identity.credentials.hashed_password.hashed_password
        original_changed_at = original_identity.credentials.password_changed_at

        new_password = "new_user_password_secret"
        identity.reset_password(new_password)

        await self.user_identity_repository.save(identity)
        await self.session.commit()

        updated_identity = await self.user_identity_repository.get_user_identity(user.id)
        updated_hash = updated_identity.credentials.hashed_password.hashed_password
        updated_changed_at = updated_identity.credentials.password_changed_at

        assert updated_hash != original_hash
        assert updated_changed_at > original_changed_at
        assert updated_identity.user_id == user.id

