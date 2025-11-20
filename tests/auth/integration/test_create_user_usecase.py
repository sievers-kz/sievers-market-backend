import pytest
from sqlalchemy.exc import IntegrityError

from src.core.users.domain.enums import UserRoleEnum


class TestCreateUserUseCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, container):
        self.usecase = container.create_user_usecase()
        self.uow = container.user_identity_unit_of_work()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_individual_user_success(self, create_user_dto):
        dto = create_user_dto(role=UserRoleEnum.INDIVIDUAL)
        await self.usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)

        assert user.id is not None
        assert user.role == UserRoleEnum.INDIVIDUAL
        assert user.business_details is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_business_user_success(self, create_user_dto):
        dto = create_user_dto(role=UserRoleEnum.BUSINESS)
        await self.usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)

        assert user.id is not None
        assert user.role == UserRoleEnum.BUSINESS
        assert user.business_details is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_user_identity_success(self, create_user_dto):
        dto = create_user_dto()
        await self.usecase.execute(dto)

        async with self.uow:
            user = await self.uow.user.get_by_user_email(dto.user.email)
            identity = await self.uow.identity.get_user_identity(user.id)

        assert identity.id is not None
        assert identity.user_id == user.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_user_on_duplicate_email(self, create_user_dto):
        dto = create_user_dto(email="duplicated@example.com")
        await self.usecase.execute(dto)

        with pytest.raises(IntegrityError):
            await self.usecase.execute(dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_user_on_duplicate_phone(self, create_user_dto):
        dto = create_user_dto(phone="87472006243")
        await self.usecase.execute(dto)

        with pytest.raises(IntegrityError):
            await self.usecase.execute(dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_user_on_duplicate_document_value(self, create_user_dto):
        dto = create_user_dto(doc_value="123456789012")
        await self.usecase.execute(dto)

        with pytest.raises(IntegrityError):
            await self.usecase.execute(dto)

