from uuid import UUID

from src.core.machinery.application.interfaces.abstract_machinery_uow import AbstractMachineryUnitOfWork


class DeleteMachineryUseCase:
    def __init__(self, unit_of_work: AbstractMachineryUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, machinery_id: UUID):
        async with self.unit_of_work as uow:
            machinery = await uow.machinery.get_by_machinery_id(machinery_id)
            machinery.delete()

            await uow.machinery.save(machinery)
            await uow.commit()
