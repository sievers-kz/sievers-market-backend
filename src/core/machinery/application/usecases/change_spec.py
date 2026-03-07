from uuid import UUID

from src.core.machinery.application.interfaces.attribute_validator import IAttributeValidator
from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.presentation.dto import ChangeMachinerySpecRequest


class ChangeMachinerySpecUseCase:
    def __init__(self, uow: IMachineryUnitOfWork, attribute_validator: IAttributeValidator):
        self.uow = uow
        self.attribute_validator = attribute_validator

    async def execute(self, machinery_id: UUID, dto: ChangeMachinerySpecRequest):
        validated_attributes = self.attribute_validator.validate(dto.subcategory_id, dto.attributes)
        async with self.uow as uow:
            machinery = await uow.machinery.get_machinery_by_id(machinery_id)
            machinery.change_spec(validated_attributes)

            await uow.machinery.save(machinery)
            await uow.commit()
