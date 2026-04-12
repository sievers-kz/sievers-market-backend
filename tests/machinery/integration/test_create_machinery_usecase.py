import pytest


class TestCreateMachineryUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_machinery_success(
        self,
        create_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert machinery is not None
        assert machinery.id == machinery_id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_machinery_limit_exceeded(
        self,
        create_machinery_usecase,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        for _ in range(5):
            await create_machinery_usecase.execute(create_customer.id, dto)

        with pytest.raises(ValueError, match="Вы достигли лимита бесплатных объявлений"):
            await create_machinery_usecase.execute(create_customer.id, dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_machinery_with_invalid_attributes(
        self,
        create_machinery_usecase,
        create_machinery_request,
        create_customer
    ):
        create_machinery_request.attributes = {"invalid_attribute": "garbage"}
        with pytest.raises(ValueError):
            await create_machinery_usecase.execute(create_customer.id, create_machinery_request)