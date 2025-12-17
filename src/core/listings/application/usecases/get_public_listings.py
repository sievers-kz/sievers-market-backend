from uuid import UUID

from src.api.listings.dto import PublicListingsPageResponse
from src.core.listings.infrastructure.filter_builder import FilterBuilderService
from src.core.shared.application.abstract_uow import AbstractListingReferenceUnitOfWork


class GetPublicListingsUseCase:
    def __init__(self, filter_builder: FilterBuilderService, unit_of_work: AbstractListingReferenceUnitOfWork):
        self.unit_of_work = unit_of_work
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
        async with self.unit_of_work as uow:
            base_filters = await uow.filter_query.get_base_filters(category_id)
            dynamic_filters = []
            if subcategory_id:
                dynamic_filters = await uow.filter_query.get_dynamic_filters(subcategory_id)
            filters = self.filter_builder.build_filters(base_filters, dynamic_filters)

            listings, total = await uow.listing_query.get_filtered_listings(
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
