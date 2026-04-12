import pytest

from src.core.machinery.domain.value_objects import Title
from src.core.machinery.infrastructure.factory import MachineryFactory
from src.core.shared.domain.enums import ListingStatus


class TestActivateMachineryUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_activate_machinery_successful(
        self,
        create_machinery_usecase,
        activate_machinery_usecase,
        deactivate_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        await deactivate_machinery_usecase.execute(create_customer.id, machinery_id)
        await activate_machinery_usecase.execute(create_customer.id, machinery_id)

        machinery = await machinery_repository.get_machinery_by_id(machinery_id)
        assert machinery.status == ListingStatus.ACTIVE

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_activate_machinery_limit_exceeded(
        self,
        create_machinery_usecase,
        activate_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        for _ in range(5):
            await create_machinery_usecase.execute(create_customer.id, dto)

        inactive_machinery = MachineryFactory.create(
            create_customer.id,
            title=Title("John Deere"),
            attibutes={},
            dto=dto
        )
        inactive_machinery.status = ListingStatus.INACTIVE
        await machinery_repository.save(inactive_machinery)

        with pytest.raises(ValueError, match="Вы достигли лимита бесплатных объявлений"):
            await activate_machinery_usecase.execute(create_customer.id, inactive_machinery.id)

    