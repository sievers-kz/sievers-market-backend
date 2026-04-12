import pytest

from src.core.machinery.presentation.dto import ChangeMachineryGeneralRequest


class TestChangeMachineryGeneralUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_general_successful(
        self,
        create_machinery_usecase,
        change_machinery_general_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer,
        brand_repository
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        brands = await brand_repository.get_all()
        brand = brands[1]

        change_machinery_general_dto = ChangeMachineryGeneralRequest(brand_id=brand.id, model="Lexion")
        await change_machinery_general_usecase.execute(machinery_id, change_machinery_general_dto)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert brand.id != dto.brand_id
        assert machinery.model == "Lexion"
