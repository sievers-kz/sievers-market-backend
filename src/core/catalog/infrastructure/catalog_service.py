from dataclasses import dataclass
from uuid import UUID

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.catalog.infrastructure.repositories.attributes import SubcategoryAttributeRepository
from src.core.catalog.infrastructure.repositories.categories import (
    CategoryRepository,
    SubcategoryRepository,
)


@dataclass(frozen=True)
class SearchAttributes:
    """Атрибуты для настроек индекса поиска.

    `filterable`: все фильтруемые ключи. `text`: из них строковые, по ним имеет смысл текстовый поиск
    (у `enumerate` в значении ключ варианта, у `reference` id, у чисел цифры).
    """

    filterable: list[str]
    text: list[str]


class CatalogService:
    """Публичный сервис каталога: проверки ссылок на каталог для других контекстов."""

    def __init__(
        self,
        category_repo: CategoryRepository,
        subcategory_repo: SubcategoryRepository,
        link_repo: SubcategoryAttributeRepository,
    ):
        self._category_repo = category_repo
        self._subcategory_repo = subcategory_repo
        self._link_repo = link_repo

    async def ensure_subcategory_in_category(self, category_id: UUID, subcategory_id: UUID) -> None:
        if await self._category_repo.get_by_id(category_id) is None:
            raise CatalogNotFoundError(field=str(category_id))

        subcategory = await self._subcategory_repo.get_by_id(subcategory_id)
        if subcategory is None or subcategory.category_id != category_id:
            raise CatalogNotFoundError(field=str(subcategory_id))

    async def get_filterable_keys(self, subcategory_id: UUID) -> set[str]:
        """Ключи атрибутов подкатегории с флагом `filterable`: только они попадают в индекс поиска."""
        return set(await self.get_filterable_types(subcategory_id))

    async def get_filterable_types(self, subcategory_id: UUID) -> dict[str, AttributeType]:
        """Фильтруемые атрибуты подкатегории с типом: по типу поиск решает, допустим ли диапазон."""
        return await self._link_repo.get_filterable_types(subcategory_id)

    async def get_search_attributes(self) -> SearchAttributes:
        attributes = await self._link_repo.get_all_filterable()
        return SearchAttributes(
            filterable=sorted(key for key, _ in attributes),
            text=sorted(key for key, attribute_type in attributes if attribute_type == AttributeType.STRING),
        )
