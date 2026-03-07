from uuid import UUID

from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.presentation.dto import ChangeMachineryPriceRequest


class ChangeMachineryPriceUseCase:
    def __init__(self, uow: IMachineryUnitOfWork):
        self.uow = uow

    async def execute(self, machinery_id: UUID, dto: ChangeMachineryPriceRequest):
        async with self.uow as uow:
            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.change_price(dto.price, dto.currency)

            await uow.machinery.save(machinery)
            await uow.commit()
