from uuid import UUID

from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork


class DeleteMachineryUseCase:
    def __init__(self, uow: IMachineryUnitOfWork):
        self.uow = uow

    async def execute(self, customer_id: UUID, machinery_id: UUID):
        async with self.uow as uow:
            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.delete()

            await uow.machinery.save(machinery)
            await uow.commit()
