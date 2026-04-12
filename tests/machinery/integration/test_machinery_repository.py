import uuid

import pytest

from src.core.machinery.domain.entities import Machinery


class TestMachineryRepository:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_machinery_by_id_success(
        self,
        create_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        machinery_id = await create_machinery_usecase.execute(create_customer.id, create_machinery_request)
        machinery = await machinery_repository.get_machinery_by_id(machinery_id)

        assert machinery is not None
        assert isinstance(machinery, Machinery)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_machinery_by_id_not_found(self, machinery_repository):
        result = await machinery_repository.get_machinery_by_id(uuid.uuid4())
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_count_customer_machinery_only_active(
        self,
        create_machinery_usecase,
        deactivate_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        ids = []
        for _ in range(3):
            machinery_id = await create_machinery_usecase.execute(create_customer.id, create_machinery_request)
            ids.append(machinery_id)

        await deactivate_machinery_usecase.execute(create_customer.id, ids[0])
        count = await machinery_repository.count_customer_machinery(create_customer.id)
        assert count == 2
