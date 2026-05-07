from uuid import UUID

from src.core.catalog.application.interfaces import ICatalogUnitOfWork
from src.core.catalog.domain.entities import Subcategory
from src.core.catalog.domain.value_objects import Attribute

from src.core.catalog.presentation.dto.subcategory import (
    CreateSubcategoryRequest,
    ChangeSubcategoryParentRequest,
    ChangeSubcategoryNameRequest,
    ReplaceSubcategoryAttributeRequest
)


class SubcategoryService:
    def __init__(self, uow: ICatalogUnitOfWork):
        self.uow = uow

    async def create(self, dto: CreateSubcategoryRequest) -> None:
        async with self.uow as uow:
            category = await uow.category.get_by_id(dto.category_id)
            if not category:
                raise ValueError("Unknown category")

            attributes = [Attribute.from_dict(attr) for attr in dto.attributes]
            subcategory = Subcategory.create(category_id=category.id, name=dto.name, attributes=attributes)

            await uow.subcategory.save(subcategory)
            await uow.commit()

    async def change_category(self, subcategory_id: UUID, dto: ChangeSubcategoryParentRequest):
        async with self.uow as uow:
            category = await uow.category.get_by_id(dto.category_id)
            if not category:
                raise ValueError("Unknown category")

            subcategory = await uow.subcategory.get_by_id(subcategory_id)
            if not subcategory:
                raise ValueError("Subcategory not found")

            subcategory.change_parent(dto.category_id)
            await uow.subcategory.save(subcategory)
            await uow.commit()

    async def change_name(self, subcategory_id: UUID, dto: ChangeSubcategoryNameRequest) -> None:
        async with self.uow as uow:
            subcategory = await uow.subcategory.get_by_id(subcategory_id)
            if not subcategory:
                raise ValueError("Subcategory not found")

            subcategory.change_name(dto.name)
            await uow.subcategory.save(subcategory)
            await uow.commit()

    async def replace_attributes(self, subcategory_id: UUID, dto: ReplaceSubcategoryAttributeRequest):
        async with self.uow as uow:
            subcategory = await uow.subcategory.get_by_id(subcategory_id)
            if not subcategory:
                raise ValueError("Subcategory not found")

            domain_attributes = [Attribute.from_dict(attr.model_dump()) for attr in dto.attributes]
            subcategory.replace_attributes(domain_attributes)

            await uow.subcategory.save(subcategory)
            await uow.commit()

    async def delete_subcategory(self, subcategory_id: UUID) -> None:
        async with self.uow as uow:
            subcategory = await uow.subcategory.get_by_id(subcategory_id)
            if not subcategory:
                raise ValueError("Subcategory not found")

            subcategory.delete()
            await uow.subcategory.save(subcategory)
            await uow.commit()

    async def validate_attributes(self, subcategory_id: UUID, attributes: list[dict]):
        async with self.uow as uow:
            subcategory = await uow.subcategory.get_by_id(subcategory_id)
            if not subcategory:
                raise ValueError("Subcategory not found")

            validated_attributes = subcategory.validate_attributes(attributes)
            return validated_attributes
