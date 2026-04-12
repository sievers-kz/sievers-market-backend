import pytest

from src.core.machinery.presentation.dto import ChangeMachinerySpecRequest


class TestChangeMachinerySpecUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_spec_successful(
        self,
        create_machinery_usecase,
        change_machinery_spec_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        change_machinery_spec_dto = ChangeMachinerySpecRequest(
            subcategory_id=dto.subcategory_id,
            attributes={
                "engine_power": 777,
                "max_speed": 96
            }
        )

        await change_machinery_spec_usecase.execute(machinery_id, change_machinery_spec_dto)
        machinery = await machinery_repository.get_machinery_by_id(machinery_id)

        assert dto.subcategory_id == machinery.subcategory_id
        assert "max_speed" in machinery.attributes

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_spec_with_invalid_attribute(
        self,
        create_machinery_usecase,
        change_machinery_spec_usecase,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        change_machinery_spec_dto = ChangeMachinerySpecRequest(
            subcategory_id=dto.subcategory_id,
            attributes={"invalid_attribute": "invalid_value"}
        )

        with pytest.raises(ValueError):
            await change_machinery_spec_usecase.execute(machinery_id, change_machinery_spec_dto)
