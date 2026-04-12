import uuid

import pytest
from werkzeug.exceptions import NotFound

from src.core.wishlist.application.usecases import add_to_wishlist


class TestGetCustomerMachineryDetailUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_customer_machinery_detail_successful(
        self,
        create_machinery_usecase,
        get_customer_machinery_detail_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        detail_response = await get_customer_machinery_detail_usecase.execute(create_customer.id, machinery_id)
        assert detail_response is not None

        assert detail_response.id == machinery_id
        assert detail_response.wishlist_total_count == 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_customer_machinery_detail_with_add_to_wishlist(
        self,
        create_machinery_usecase,
        add_to_wishlist_usecase,
        get_customer_machinery_detail_usecase,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        await add_to_wishlist_usecase.execute(create_customer.id, machinery_id)

        detail_response = await get_customer_machinery_detail_usecase.execute(create_customer.id, machinery_id)
        assert detail_response is not None

        assert detail_response.id == machinery_id
        assert detail_response.wishlist_total_count == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_customer_machinery_detail_not_found(
        self,
        get_customer_machinery_detail_usecase,
        create_customer
    ):
        with pytest.raises(ValueError, match="Объявление не найдено. Возможно оно было помещено в архив или удалено"):
            await get_customer_machinery_detail_usecase.execute(create_customer.id, uuid.uuid4())
