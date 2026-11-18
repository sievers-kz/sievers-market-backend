from uuid import UUID

from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import UUID as PsqlUUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.infrastructure.models import Category, Subcategory
from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.customer.infrastructure.models import Organization
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.models import Listing
from src.core.listing.presentation.dto import (
    ListingCardResponse,
    ListingDetailResponse,
    MyListingCardResponse,
    MyListingsSort,
    MyListingsStatus,
)
from src.core.references.infrastructure.models import City
from src.core.shared.infrastructure.services.query_service import QueryService


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
        statement = (
            select(
                Listing.id,
                Listing.organization_id.label("owner_id"),
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                Listing.description,
                Listing.gallery,
                Listing.attributes,
            )
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .where(Listing.id == listing_id, Listing.status == ListingStatus.ACTIVE)
        )

        query_result = await self._session.execute(statement)
        result = query_result.mappings().one_or_none()

        if not result:
            raise ListingNotFoundError()

        return ListingDetailResponse.model_validate(result)
