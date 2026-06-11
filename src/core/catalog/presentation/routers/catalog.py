from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Query

from src.configuration.dependencies.container import ApplicationContainer
from src.core.catalog.infrastructure.query import CatalogQueryService
from src.core.catalog.presentation.dto.catalog import AttributeResponse, RubricResponse, ListingCardResponse, \
    ListingDetailResponse, VendorCardResponse, DetailVendorResponse
from src.core.catalog.presentation.routers.subcategory import subcategory_router
from src.core.shared.presentation.dto import PaginatedResponse

catalog_router = APIRouter(prefix="/api/v1/catalog", tags=["Catalog"])
catalog_router.include_router(subcategory_router)


@catalog_router.get("/{subcategory_id}/form", response_model=AttributeResponse)
@inject
async def get_form(
    subcategory_id: UUID,
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ]
):
    return await service.get_subcategory_attributes(subcategory_id)


@catalog_router.get("/tree", response_model=list[RubricResponse])
@inject
async def get_category_tree(
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ]
):
    return await service.get_category_tree()


@catalog_router.get("/listing/list", response_model=PaginatedResponse[ListingCardResponse])
@inject
async def get_listings_card(
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ],
    category_id: UUID = Query(alias="category_id"),
    subcategory_id: UUID | None = Query(None, alias="subcategory_id"),
    page: int = Query(1, alias="page"),
    limit: int = Query(20, alias="limit"),
):
    return await service.get_listings_card(category_id, subcategory_id, page, limit)


@catalog_router.get("/listing/{listing_id}", response_model=ListingDetailResponse)
@inject
async def get_listing_details(
    listing_id: UUID,
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ]
):
    return await service.get_listing_details(listing_id)


@catalog_router.get("/vendor/list", response_model=PaginatedResponse[VendorCardResponse])
@inject
async def get_vendor_cards(
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ],
    page: int = Query(1, alias="page"),
    limit: int = Query(20, alias="limit"),
):
    return await service.get_vendors_card(page, limit)


@catalog_router.get("/vendor/{vendor_id}", response_model=DetailVendorResponse)
@inject
async def get_vendor_details(
    vendor_id: UUID,
    service: Annotated[
        CatalogQueryService,
        Depends(
            Provide[
                ApplicationContainer.catalog.query_service
            ]
        )
    ]
):
    return await service.get_vendor_details(vendor_id)
