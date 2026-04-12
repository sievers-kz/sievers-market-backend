from uuid import UUID

from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.domain.enums import ACTIVE_LISTINGS_LIMIT


class ActivateMachineryUseCase:
    def __init__(self, uow: IMachineryUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, machinery_id: UUID):
        async with self.uow as uow:
            current_count = await uow.machinery.count_customer_machinery(customer_id)
            if current_count >= ACTIVE_LISTINGS_LIMIT:
                raise ValueError("Вы достигли лимита бесплатных объявлений")

            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.activate()

            await uow.machinery.save(machinery)
            await uow.commit()
