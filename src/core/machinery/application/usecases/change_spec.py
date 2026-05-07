from uuid import UUID

from src.core.catalog.application.services.subcategory import SubcategoryService
from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.presentation.dto import ChangeMachinerySpecRequest


class ChangeMachinerySpecUseCase:
    def __init__(
        self,
        uow: IMachineryUnitOfWork,
        subcategory_service: SubcategoryService
    ):
        self.uow = uow
        self.subcategory_service = subcategory_service

    async def execute(self, machinery_id: UUID, dto: ChangeMachinerySpecRequest):
        validated_attributes = await self.subcategory_service.validate_attributes(dto.subcategory_id, dto.attributes)
        async with self.uow as uow:
            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.change_spec(validated_attributes)

            await uow.machinery.save(machinery)
            await uow.commit()
