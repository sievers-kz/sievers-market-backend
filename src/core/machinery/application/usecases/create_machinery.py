from uuid import UUID

from src.api.machinery.dto import CreateMachinery
from src.core.machinery.application.interfaces.abstract_attribute_validator import AbstractAttributeValidator
from src.core.machinery.application.interfaces.abstract_machinery_uow import AbstractMachineryUnitOfWork
from src.core.machinery.infrastructure.factory import MachineryFactory


class CreateMachineryUseCase:
    def __init__(
        self,
        unit_of_work: AbstractMachineryUnitOfWork,
        attribute_validator: AbstractAttributeValidator
    ):
        self.unit_of_work = unit_of_work
        self.attribute_validator = attribute_validator

    async def execute(self, dto: CreateMachinery, seller_id: UUID):
        async with self.unit_of_work as uow:
            validated_attributes = await self.attribute_validator.validate(dto.subcategory_id, dto.attributes,)

            data = dto.model_dump(exclude={"attributes"})
            machinery = MachineryFactory.create(seller_id=seller_id, attributes=validated_attributes, **data)

            await uow.machinery.save(machinery)
            await uow.commit()

