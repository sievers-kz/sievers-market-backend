from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import select, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.dialects.postgresql import UUID as PsqlUUID

from src.core.catalog.application.interfaces.query_service import ICatalogQueryService
from src.core.catalog.domain.enums import CatalogStatus
from src.core.catalog.infrastructure.models import Subcategory, Rubric, Category
from src.core.catalog.presentation.dto.catalog import AttributeResponse, RubricResponse, ListingCardResponse, \
    ListingDetailResponse, VendorCardResponse
from src.core.catalog.presentation.dto.subcategory import Attribute
from src.core.customer.infrastructure.models import Customer
from src.core.iam.infrastructure.models import Account
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.infrastructure.models import Listing
from src.core.references.infrastructure.models import City
from src.core.shared.infrastructure.services.query_service import QueryService
from src.core.vendor.infrastructure.models import Vendor


class CatalogQueryService(QueryService, ICatalogQueryService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_subcategory_attributes(self, subcategory_id: UUID) -> list[Attribute]:
        statement = (
            select(Subcategory, Rubric)
            .join(Category, Subcategory.category_id == Category.id)
            .join(Rubric, Category.rubric_id == Rubric.id)
            .options(
                load_only(Subcategory.attributes),
                load_only(Rubric.attributes),
            ).where(Subcategory.id == subcategory_id)
        )

        query_result = await self._session.execute(statement)
        result = query_result.first()
        subcategory, rubric = result

        return AttributeResponse(
            base_fields=rubric.attributes,
            dynamic_fields=subcategory.attributes,
        )

    async def get_category_tree(self) -> list[RubricResponse]:
        statement = (
            select(Rubric)
            .options(
                load_only(Rubric.id, Rubric.name),
                joinedload(Rubric.categories).options(
                    load_only(Category.id, Category.rubric_id, Category.name),
                    joinedload(Category.subcategories).options(
                        load_only(Subcategory.id, Subcategory.category_id, Subcategory.name),
                    )
                )
            ).where(Rubric.status == CatalogStatus.ACTIVE)
        )

        query_result = await self._session.execute(statement)
        results = query_result.scalars().unique().all()
        return TypeAdapter(list[RubricResponse]).validate_python(results)

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
                Customer.last_name.label("last_name"),
                Customer.first_name.label("first_name"),
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                cast(Listing.gallery[0]["media_id"].as_string(), PsqlUUID).label("preview_image")
            )
            .join(Customer, Listing.owner_id == Customer.account_id)
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .where(
                Listing.category_id == category_id,
                Listing.status == ListingStatus.ACTIVE
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
                Listing.owner_id,
                Account.email,
                Account.phone,
                Customer.last_name.label("last_name"),
                Customer.first_name.label("first_name"),
                Subcategory.name.label("subcategory"),
                Listing.title,
                Listing.price,
                Listing.currency,
                City.name.label("city"),
                Listing.description,
                Listing.gallery,
                Listing.attributes,
            )
            .join(Account, Listing.owner_id == Account.id)
            .join(Customer, Listing.owner_id == Customer.account_id)
            .join(Subcategory, Listing.subcategory_id == Subcategory.id)
            .join(City, Listing.city_id == City.id)
            .where(
                Listing.id == listing_id,
                Listing.status == ListingStatus.ACTIVE
            )
        )

        query_result = await self._session.execute(statement)
        result = query_result.mappings().one_or_none()

        if not result:
            return None

        return ListingDetailResponse.model_validate(result)

    async def get_vendors_card(self, page: int = 1, limit: int = 20) -> list[VendorCardResponse]:
        statement = (
            select(
                Vendor.id.label("vendor_id"),
                Vendor.is_verified,
                Vendor.legal_name,
                Vendor.shop_name,
                Vendor.logotype
            ).where(Vendor.is_verified == True)
        )

        return await self.paginate(
            statement=statement,
            schema=VendorCardResponse,
            page=page,
            limit=limit,
        )
