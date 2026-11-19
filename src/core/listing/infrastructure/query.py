from uuid import UUID

from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import UUID as PsqlUUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.catalog.infrastructure.models import Category, Subcategory, SubcategoryAttribute
from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.models import Organization
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.models import Listing
from src.core.listing.presentation.dto import (
    ListingCardResponse,
    ListingDetailResponse,
    ListingSpecGroup,
    ListingSpecItem,
    MyListingCardResponse,
    MyListingsSort,
    MyListingsStatus,
)
from src.core.references.infrastructure.models import Brand, City, Color, OriginCountry
from src.core.shared.infrastructure.services.query_service import QueryService

# `source` атрибута типа `reference` -> справочник, из которого берётся название.
REFERENCE_MODELS = {"brand": Brand, "country": OriginCountry, "color": Color}


class ListingQueryService(QueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_listings_card(
        self,
        category_id: UUID,
        subcategory_id: UUID | None,
        page: int = 1,
        limit: int = 20,
    ) -> list:
        """Карточки каталога: активные объявления категории, новые сверху.

        Join на `Organization` осознанное исключение из ADR 004 (как в `get_my_listings`): это read-запрос.
        Название организации: название магазина, а если его нет, юридическое название.
        `condition` это ключ варианта атрибута (`new`, `used`); у подкатегорий без такого атрибута он `None`.
        """
        statement = self._card_statement().where(
            Listing.category_id == category_id,
            Listing.status == ListingStatus.ACTIVE,
        )

        if subcategory_id is not None:
            statement = statement.where(Listing.subcategory_id == subcategory_id)

        # Второй ключ делает порядок стабильным между страницами при одинаковом `created_at`.
        statement = statement.order_by(Listing.created_at.desc(), Listing.id.desc())

        return await self.paginate(
            statement=statement,
            schema=ListingCardResponse,
            page=page,
            limit=limit,
        )

    async def get_listings_by_ids(self, listing_ids: list[UUID]) -> list[ListingCardResponse]:
        """Карточки активных объявлений по списку id (для поиска). Порядок не гарантирован, его задаёт вызывающий.

        Объявление, которое успело стать неактивным после индексации, просто не вернётся.
        """
        if not listing_ids:
            return []

        statement = self._card_statement().where(
            Listing.id.in_(listing_ids),
            Listing.status == ListingStatus.ACTIVE,
        )
        result = await self._session.execute(statement)
        return [ListingCardResponse.model_validate(row) for row in result.mappings().all()]

    @staticmethod
    def _card_statement():
        """Колонки и join'ы карточки каталога; общие для каталога и поиска, чтобы формат карточки был один.

        Join на `Organization` осознанное исключение из ADR 004: это read-запрос.
        """
        return (
            select(
                Listing.id,
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                cast(Listing.gallery[0]["media_id"].as_string(), PsqlUUID).label("preview_image"),
                Listing.created_at,
                func.coalesce(Organization.shop_name, Organization.legal_name).label("organization_name"),
                Listing.attributes["condition"].as_string().label("condition"),
            )
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .join(Organization, Listing.organization_id == Organization.id)
        )

    async def get_my_listings(
        self,
        owner_id: UUID,
        status: MyListingsStatus | None = None,
        organization_id: UUID | None = None,
        category_id: UUID | None = None,
        sort: MyListingsSort = MyListingsSort.NEWEST,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        """Объявления всех организаций владельца (читаем из Postgres: индекс поиска отстаёт и неактивных в нём нет).

        Join на `Organization` осознанное исключение из ADR 004: это read-запрос, а владельца объявления
        определяет именно организация. Удалённые объявления не возвращаются.
        """
        if organization_id is not None:
            is_owner_stmt = select(Organization.id).where(
                Organization.id == organization_id,
                Organization.owner_id == owner_id,
            )
            if (await self._session.execute(is_owner_stmt)).first() is None:
                raise OrganizationNotFoundError()

        statement = (
            select(
                Listing.id,
                Listing.title,
                Listing.price,
                Listing.currency,
                Listing.status,
                Category.name.label("category"),
                Subcategory.name.label("subcategory"),
                Listing.organization_id,
                func.coalesce(Organization.shop_name, Organization.legal_name).label("organization_name"),
                City.name.label("city"),
                cast(Listing.gallery[0]["media_id"].as_string(), PsqlUUID).label("preview_image"),
                Listing.created_at,
            )
            .join(Organization, Listing.organization_id == Organization.id)
            .join(Category, Listing.category_id == Category.id)
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .outerjoin(City, Listing.city_id == City.id)
            .where(
                Organization.owner_id == owner_id,
                Listing.status != ListingStatus.DELETED,
            )
        )

        if status is not None:
            statement = statement.where(Listing.status == ListingStatus(status.value))
        if organization_id is not None:
            statement = statement.where(Listing.organization_id == organization_id)
        if category_id is not None:
            statement = statement.where(Listing.category_id == category_id)

        if sort == MyListingsSort.OLDEST:
            statement = statement.order_by(Listing.created_at.asc(), Listing.id.asc())
        else:
            statement = statement.order_by(Listing.created_at.desc(), Listing.id.desc())

        return await self.paginate(
            statement=statement,
            schema=MyListingCardResponse,
            page=page,
            limit=limit,
        )

    async def get_listing_details(self, listing_id: UUID) -> ListingDetailResponse:
        """Детальная карточка активного объявления: продавец и характеристики, готовые к показу.

        Join'ы на `Organization` и модели каталога осознанное исключение из ADR 004 (как в `_card_statement`):
        это read-запрос. Сырые `attributes` остаются в ответе для совместимости.
        """
        statement = (
            select(
                Listing.id,
                Listing.organization_id.label("owner_id"),
                Listing.category_id,
                Category.name.label("category"),
                Listing.subcategory_id,
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                Listing.description,
                Listing.gallery,
                Listing.attributes,
                Listing.attributes["condition"].as_string().label("condition"),
                Listing.created_at,
                func.coalesce(Organization.shop_name, Organization.legal_name).label("seller_name"),
                Organization.contact_phone.label("seller_phone"),
                Organization.contact_email.label("seller_email"),
                Organization.logo_media_id.label("seller_logo_media_id"),
            )
            .join(Category, Listing.category_id == Category.id)
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .join(Organization, Listing.organization_id == Organization.id)
            .where(Listing.id == listing_id, Listing.status == ListingStatus.ACTIVE)
        )

        query_result = await self._session.execute(statement)
        result = query_result.mappings().one_or_none()

        if not result:
            raise ListingNotFoundError()

        specs = await self._build_specs(result["subcategory_id"], result["attributes"] or {})
        return ListingDetailResponse.model_validate(
            {
                **result,
                "seller": {
                    "organization_id": result["owner_id"],
                    "name": result["seller_name"],
                    "phone": result["seller_phone"],
                    "email": result["seller_email"],
                    "logo_media_id": result["seller_logo_media_id"],
                },
                "specs": specs,
            }
        )

    async def _build_specs(self, subcategory_id: UUID, attributes: dict) -> list[ListingSpecGroup]:
        """Значения атрибутов с подписями, по группам и в порядке формы.

        Пустые значения и ключи, которых больше нет в настройке подкатегории, пропускаются.
        Ссылки на справочники (`reference`) заменяются названиями одним запросом на справочник.
        """
        links_result = await self._session.execute(
            select(SubcategoryAttribute)
            .where(SubcategoryAttribute.subcategory_id == subcategory_id)
            .options(
                joinedload(SubcategoryAttribute.attribute),
                joinedload(SubcategoryAttribute.group),
                joinedload(SubcategoryAttribute.unit),
            )
        )
        links = [
            link
            for link in links_result.scalars().unique().all()
            if attributes.get(link.attribute.key) not in (None, "", [])
        ]
        links.sort(key=lambda link: (link.group.position, link.position))

        reference_names = await self._load_reference_names(links, attributes)

        groups: dict[UUID, ListingSpecGroup] = {}
        for link in links:
            definition = link.attribute
            value = self._display_value(definition, attributes[definition.key], reference_names)
            if value is None:
                continue
            group = groups.setdefault(
                link.group.id, ListingSpecGroup(key=link.group.key, label=link.group.label, items=[])
            )
            group.items.append(
                ListingSpecItem(
                    key=definition.key,
                    label=definition.label,
                    value=value,
                    unit=link.unit.label if link.unit else None,
                )
            )
        return list(groups.values())

    async def _load_reference_names(self, links: list, attributes: dict) -> dict[str, str]:
        """Названия из справочников по id, общий словарь `str(id) -> name` для всех `reference` атрибутов."""
        ids_by_source: dict[str, set[UUID]] = {}
        for link in links:
            definition = link.attribute
            if definition.type != AttributeType.REFERENCE or definition.source not in REFERENCE_MODELS:
                continue
            try:
                ids_by_source.setdefault(definition.source, set()).add(UUID(str(attributes[definition.key])))
            except ValueError:
                continue

        names: dict[str, str] = {}
        for source, ids in ids_by_source.items():
            model = REFERENCE_MODELS[source]
            rows = await self._session.execute(select(model.id, model.name).where(model.id.in_(ids)))
            names.update({str(row_id): name for row_id, name in rows.all()})
        return names

    @staticmethod
    def _display_value(definition, raw, reference_names: dict[str, str]) -> str | int | float | None:
        """Значение для показа; `None`, если показать нечего (неизвестный вариант или удалённая запись справочника)."""
        if definition.type == AttributeType.ENUMERATE:
            labels = {option["key"]: option["label"] for option in definition.options or []}
            return labels.get(raw)
        if definition.type == AttributeType.REFERENCE:
            return reference_names.get(str(raw))
        if definition.type == AttributeType.BOOLEAN:
            return "Да" if raw else "Нет"
        if isinstance(raw, bool) or not isinstance(raw, (str, int, float)):
            return None
        return raw
