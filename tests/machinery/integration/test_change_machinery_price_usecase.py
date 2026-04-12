import pytest

from src.core.machinery.presentation.dto import ChangeMachineryPriceRequest
from src.core.shared.domain.enums import PriceCurrency


class TestChangeMachineryPriceUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_change_machinery_price_successful(
        self,
        create_machinery_usecase,
        change_machinery_price_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        change_machinery_price_dto = ChangeMachineryPriceRequest(price=1_000_000, currency=PriceCurrency.USD)
        await change_machinery_price_usecase.execute(machinery_id, change_machinery_price_dto)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert machinery.currency == PriceCurrency.USD
        assert machinery.price.value < dto.price
