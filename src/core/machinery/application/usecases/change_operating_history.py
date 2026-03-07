from uuid import UUID

from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.presentation.dto import ChangeOperatingHistoryRequest


class ChangeOperatingHistoryUseCase:
    def __init__(self, uow: IMachineryUnitOfWork):
        self.uow = uow

    async def execute(self, machinery_id: UUID, dto: ChangeOperatingHistoryRequest):
        async with self.uow as uow:
            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.change_operating_history(dto.year_of_issue, dto.condition)

            await uow.machinery.save(machinery)
            await uow.commit()
