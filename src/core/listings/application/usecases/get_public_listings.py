from uuid import UUID

from src.api.listings.dto import PublicListingsPageResponse
from src.core.listings.application.abstract_listing_query_context import AbstractListingQueryContext
from src.core.listings.infrastructure.filter_builder import FilterBuilderService


class GetPublicListingsUseCase:
    def __init__(self, filter_builder: FilterBuilderService, query_service: AbstractListingQueryContext):
        self.query_service = query_service
        self.filter_builder = filter_builder

    async def execute(
        self,
        category_id: UUID,
        subcategory_id: UUID | None,
        min_price: int | None,
        max_price: int | None,
        page: int,
        page_size: int,
        applied_dynamic_filters: dict | None
    ):
        async with self.query_service as query:
            base_filters = await query.filter.get_base_filters(category_id)
            dynamic_filters = []
            if subcategory_id:
                dynamic_filters = await query.filter.get_dynamic_filters(subcategory_id)
            filters = self.filter_builder.build_filters(base_filters, dynamic_filters)

            listings, total = await query.listing.get_filtered_listings(
                category_id=category_id,
                subcategory_id=subcategory_id,
                min_price=min_price,
                max_price=max_price,
                page=page,
                page_size=page_size,
                applied_dynamic_filters=applied_dynamic_filters
            )

            return PublicListingsPageResponse(
                filters=filters,
                listings=listings,
                pagination={
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": (total + page_size - 1) // page_size
                }
            )
