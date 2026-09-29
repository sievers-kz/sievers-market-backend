from uuid import UUID

from src.core.shared.presentation.dto import DTO


class OriginCountryResponse(DTO):
    id: UUID
    name: str


class CreateOriginCountryRequest(DTO):
    name: str


class UpdateOriginCountryRequest(DTO):
    name: str
