from uuid import UUID

from src.core.shared.presentation.dto import DTO


class CountryResponse(DTO):
    id: UUID
    name: str


class CreateCountryRequest(DTO):
    name: str


class UpdateCountryRequest(DTO):
    name: str
