from uuid import UUID

from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.catalog.infrastructure.repositories.categories import (
    CategoryRepository,
    SubcategoryRepository,
)


class CatalogService:
    """Публичный сервис каталога: проверки ссылок на каталог для других контекстов."""

    def __init__(
        self,
        category_repo: CategoryRepository,
        subcategory_repo: SubcategoryRepository,
    ):
        self._category_repo = category_repo
        self._subcategory_repo = subcategory_repo

    async def ensure_subcategory_in_category(self, category_id: UUID, subcategory_id: UUID) -> None:
        if await self._category_repo.get_by_id(category_id) is None:
            raise CatalogNotFoundError(field=str(category_id))

        subcategory = await self._subcategory_repo.get_by_id(subcategory_id)
        if subcategory is None or subcategory.category_id != category_id:
            raise CatalogNotFoundError(field=str(subcategory_id))
