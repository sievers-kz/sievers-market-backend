from uuid import UUID

from src.api.machinery.dto import UpdateMachinery
from src.core.machinery.application.interfaces.abstract_attribute_validator import AbstractAttributeValidator
from src.core.machinery.application.interfaces.abstract_machinery_uow import AbstractMachineryUnitOfWork


class UpdateMachineryUseCase:
    def __init__(
        self,
        unit_of_work: AbstractMachineryUnitOfWork,
        attribute_validator: AbstractAttributeValidator
    ):
        self.unit_of_work = unit_of_work
        self.attribute_validator = attribute_validator

    async def execute(self, machinery_id: UUID, dto: UpdateMachinery):
        validated_attributes = await self.attribute_validator.validate(dto.subcategory_id, dto.attributes)

        async with self.unit_of_work as uow:
            machinery = await uow.machinery.get_by_machinery_id(machinery_id)
            if not machinery:
                raise ValueError("Machinery not found")

            update_data = dto.model_dump(exclude={"attributes"})
            machinery.update(validated_attributes, **update_data)

            await uow.machinery.save(machinery)
            await uow.commit()
