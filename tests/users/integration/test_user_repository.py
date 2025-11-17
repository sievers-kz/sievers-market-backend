import uuid

import pytest

from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum
from src.core.users.infrastructure.user_repository import UserRepository


class TestUserRepository:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, database_session, create_domain_user_from_dto):
        self.user_repository = UserRepository(database_session)
        self.create_user = create_domain_user_from_dto
        self.session = database_session

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_by_id_success(self):
        user = self.create_user(email="test.get_user_by_id.success@mail.ru")
        await self.user_repository.save(user)
        await self.session.commit()

        found_user = await self.user_repository.get_user_by_id(user.id)

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email.value == "test.get_user_by_id.success@mail.ru"
        assert found_user.is_active is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_by_id_not_found(self):
        non_existent_user_id = uuid.uuid4()
        found_user = await self.user_repository.get_user_by_id(non_existent_user_id)

        assert found_user is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_user_email_success(self):
        email = "test.get_user_by_email.success@example.com"
        user = self.create_user(email=email)
        await self.user_repository.save(user)
        await self.session.commit()

        found_user = await self.user_repository.get_by_user_email(email)

        assert found_user is not None
        assert found_user.email.value == email

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_user_email_not_found(self):
        non_existent_email = "test.get_user_nonexistent@example.com"
        found_user = await self.user_repository.get_by_user_email(non_existent_email)

        assert found_user is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_user_with_profile(self):
        user = self.create_user(email="test.save_user_with_profile@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        found_user = await self.user_repository.get_user_by_id(user.id)

        assert found_user is not None
        assert found_user.profile.fullname.first_name == "Мейржан"
        assert found_user.profile.fullname.last_name == "Бисенов"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_user_with_business_details(self):
        user = self.create_user(role=UserRoleEnum.BUSINESS, email="test.save.business.user@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        found_user = await self.user_repository.get_user_by_id(user.id)

        assert found_user is not None
        assert found_user.business_details.business_type == BusinessTypeEnum.IP
        assert found_user.business_details.organization_fullname.value == "BEST AGROW"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_updates_existing_user(self):
        user = self.create_user(email="test.save.updated.user@example.com")
        await self.user_repository.save(user)
        await self.session.commit()

        user.confirm_user()
        await self.user_repository.save(user)
        await self.session.commit()

        found_user = await self.user_repository.get_user_by_id(user.id)
        assert found_user.is_active is True
