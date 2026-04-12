import pytest

from src.core.machinery.domain.enums import MachineryCondition
from src.core.machinery.presentation.dto import ChangeOperatingHistoryRequest


class TestChangeMachineryOperatingHistoryUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_operating_history_successful(
        self,
        create_machinery_usecase,
        change_machinery_operating_history_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        change_machinery_operating_history_dto = ChangeOperatingHistoryRequest(
            year_of_issue=1994,
            condition=MachineryCondition.USED
        )
        await change_machinery_operating_history_usecase.execute(machinery_id, change_machinery_operating_history_dto)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert machinery.year_of_issue.value < dto.year_of_issue
        assert machinery.condition != dto.condition
