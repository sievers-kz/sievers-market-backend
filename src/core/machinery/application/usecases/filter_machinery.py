from typing import Any
from uuid import UUID

from src.core.machinery.application.interfaces.abstract_machinery_reader import AbstractMachineryReader


class FilterMachineryUseCase:
    def __init__(self, machinery_reader: AbstractMachineryReader):
        self.machinery_reader = machinery_reader

    async def execute(
        self,
        category_id: UUID | None,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        city_id: UUID | None,
        dynamic_filters: dict[str, Any] | None,
        page: int = 1,
        limit: int = 20
    ):
        return await self.machinery_reader.filter(
            category_id=category_id,
            subcategory_id=subcategory_id,
            min_price=min_price,
            max_price=max_price,
            city_id=city_id,
            dynamic_filters=dynamic_filters,
            page=page,
            limit=limit
        )

