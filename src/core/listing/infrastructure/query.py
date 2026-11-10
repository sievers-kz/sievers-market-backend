from uuid import UUID

from sqlalchemy import cast, select
from sqlalchemy.dialects.postgresql import UUID as PsqlUUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.infrastructure.models import Subcategory
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.infrastructure.models import Listing
from src.core.listing.presentation.dto import ListingCardResponse, ListingDetailResponse
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
        statement = (
            select(
                Listing.id,
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                cast(Listing.gallery[0]["media_id"].as_string(), PsqlUUID).label("preview_image"),
            )
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .where(
                Listing.category_id == category_id,
                Listing.status == ListingStatus.ACTIVE,
            )
        )

        if subcategory_id is not None:
            statement = statement.where(Listing.subcategory_id == subcategory_id)

        return await self.paginate(
            statement=statement,
            schema=ListingCardResponse,
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
