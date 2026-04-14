from src.core.references.presentation.dto import BrandDTO
from src.core.references.application.interfaces.abstract_brand_repository import AbstractBrandRepository


class GetBrandsUseCase:
    def __init__(self, repository: AbstractBrandRepository):
        self.repository = repository

    async def execute(self):
        brands = await self.repository.get_all()
        return [BrandDTO.model_validate(brand, from_attributes=True) for brand in brands]
