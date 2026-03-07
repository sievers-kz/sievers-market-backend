from uuid import UUID

from src.core.machinery.application.interfaces.attribute_validator import IAttributeValidator
from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.infrastructure.factory import MachineryFactory
from src.core.machinery.presentation.dto import CreateMachineryRequest


class CreateMachineryUseCase:
    def __init__(self, uow: IMachineryUnitOfWork, attribute_validator: IAttributeValidator):
        self.uow = uow
        self.attribute_validator = attribute_validator

    async def execute(self, customer_id: UUID, dto: CreateMachineryRequest):
        validated_attributes = await self.attribute_validator.validate(dto.subcategory_id, dto.attributes)
        async with self.uow as uow:
            current_count = await uow.machinery.count_customer_machinery(customer_id)
            if current_count >= 5:
                raise ValueError("Вы достигли лимита бесплатных объявлений")

            clean_data = dto.model_dump(exclude={"attributes"})
            machinery = MachineryFactory.create(customer_id=customer_id, attributes=validated_attributes, **clean_data)

            await uow.machinery.save(machinery)
            await uow.commit()

            return machinery.id
