from uuid import UUID

from sqlalchemy import cast, desc, select
from sqlalchemy.dialects.postgresql import UUID as PsqlUUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.catalog.infrastructure.models import Subcategory
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.infrastructure.models import Listing
from src.core.references.infrastructure.models import City
from src.core.shared.infrastructure.services.query_service import QueryService
from src.core.vendor.presentation.dto import (
    VendorListingCardsResponse,
)


class VendorCabinetQueryService(QueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_vendor_listing_cards_by_status(
        self,
        vendor_id: UUID,
        status: ListingStatus,
        page: int = 1,
        limit: int = 10,
    ) -> list[VendorListingCardsResponse]:
        statement = (
            select(
                Listing.id.label("listing_id"),
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                Listing.updated_at,
                City.name.label("city"),
                cast(Listing.gallery[0]["media_id"].as_string(), PsqlUUID).label(
                    "preview_image"
                ),
            )
            .select_from(Listing)
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .where(Listing.owner_id == vendor_id, Listing.status == status)
            .order_by(desc(Listing.updated_at))
        )

        return await self.paginate(
            statement=statement,
            schema=VendorListingCardsResponse,
            page=page,
            limit=limit,
        )
