from uuid import UUID

from src.core.shared.presentation.dto import DTO


class BrandResponse(DTO):
    id: UUID
    name: str


class CreateBrandRequest(DTO):
    name: str


class UpdateBrandRequest(DTO):
    name: str
