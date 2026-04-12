import pytest

from src.core.machinery.presentation.dto import ChangeMachineryDescriptionRequest


class TestChangeMachineryDescriptionUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_description_successful(
        self,
        create_machinery_usecase,
        change_machinery_description_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        change_machinery_description_dto = ChangeMachineryDescriptionRequest(description="Changed machinery description")
        await change_machinery_description_usecase.execute(machinery_id, change_machinery_description_dto)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert machinery.description.value != dto.description

