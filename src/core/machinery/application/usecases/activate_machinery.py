from uuid import UUID

from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork


class ActivateMachineryUseCase:
    def __init__(self, uow: IMachineryUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, machinery_id: UUID):
        async with self.uow as uow:
            current_count = await uow.machinery.count_customer_machinery(customer_id)
            if current_count > 5:
                raise ValueError("Превышен лимит активных бесплатных объявлений (максимально 5)")

            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.activate()

            await uow.machinery.save(machinery)
            await uow.commit()
