from uuid import UUID

from src.core.machinery.application.interfaces.attribute_validator import IAttributeValidator
from src.core.machinery.application.interfaces.uow import IMachineryUnitOfWork
from src.core.machinery.domain.enums import ACTIVE_LISTINGS_LIMIT
from src.core.machinery.domain.value_objects import Title
from src.core.machinery.infrastructure.factory import MachineryFactory
from src.core.machinery.presentation.dto import CreateMachineryRequest
from src.core.references.application.interfaces.abstract_brand_repository import AbstractBrandRepository


class CreateMachineryUseCase:
    def __init__(
        self,
        uow: IMachineryUnitOfWork,
        attribute_validator: IAttributeValidator,
        brand_repository: AbstractBrandRepository
    ):
        self.uow = uow
        self.attribute_validator = attribute_validator
        self.brand_repository = brand_repository

    async def execute(self, customer_id: UUID, dto: CreateMachineryRequest):
        validated_attributes = await self.attribute_validator.validate(dto.subcategory_id, dto.attributes)
        brand = await self.brand_repository.get_by_id(dto.brand_id)
        title = Title.create(brand_name=brand.name, model=dto.model)

        async with self.uow as uow:
            current_count = await uow.machinery.count_customer_machinery(customer_id)
            if current_count >= ACTIVE_LISTINGS_LIMIT:
                raise ValueError("Вы достигли лимита бесплатных объявлений")

            machinery = MachineryFactory.create(customer_id, title, validated_attributes, dto)

            await uow.machinery.save(machinery)
            await uow.commit()

            return machinery.id
