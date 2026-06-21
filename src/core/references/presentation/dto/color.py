from uuid import UUID

from src.core.shared.presentation.dto import DTO


class ColorResponse(DTO):
    id: UUID
    name: str
    hex: str


class CreateColorRequest(DTO):
    name: str
    hex: str


class UpdateColorRequest(DTO):
    name: str | None = None
    hex: str | None = None
