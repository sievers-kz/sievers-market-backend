from uuid import UUID

from src.core.references.application.interfaces.abstract_uow import IReferenceUnitOfWork
from src.core.references.presentation.dto.brand import UpdateBrandRequest, CreateBrandRequest, BrandResponse

from src.core.references.domain.entities import Brand


class BrandService:
    def __init__(self, uow: IReferenceUnitOfWork):
        self.uow = uow

    async def get_brand_by_id(self, brand_id: UUID):
        async with self.uow as uow:
            brand = await uow.brand.get_by_id(brand_id)
            return BrandResponse.model_validate(brand)

    async def get_brand_list(self):
        async with self.uow as uow:
            brand_list = await uow.brand.get_all()
            return [BrandResponse.model_validate(brand) for brand in brand_list]

    async def create_brand(self, dto: CreateBrandRequest) -> None:
        async with self.uow as uow:
            brand = Brand.create(name=dto.name)
            await uow.brand.save(brand)
            await uow.commit()

    async def update_brand(self, brand_id: UUID, dto: UpdateBrandRequest) -> None:
        async with self.uow as uow:
            brand = await uow.brand.get_by_id(brand_id)
            brand.update(name=dto.name)

            await uow.brand.save(brand)
            await uow.commit()

    async def delete_brand(self, brand_id: UUID) -> None:
        async with self.uow as uow:
            await uow.brand.delete(brand_id)
            await uow.commit()

