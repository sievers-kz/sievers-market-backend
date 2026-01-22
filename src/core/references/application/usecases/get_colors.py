from src.api.reference.dto import ColorDTO
from src.core.references.application.interfaces.abstract_color_repository import AbstractColorRepository


class GetColorsUseCase:
    def __init__(self, repository: AbstractColorRepository):
        self.repository = repository

    async def execute(self):
        colors = await self.repository.get_all()
        return [ColorDTO.model_validate(color, from_attributes=True) for color in colors]
