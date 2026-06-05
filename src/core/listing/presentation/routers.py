from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security

from src.configuration.dependencies.container import ApplicationContainer
from src.core.listing.application.usecases import CreateListingUseCase, ChangeListingAttributeUseCase, \
    ChangeListingPriceUseCase, ChangeListingLocationUseCase, ChangeListingDescriptionUseCase
from src.core.listing.presentation.dto import CreateListingRequest, ChangeListingAttributeRequest, \
    ChangeListingDescriptionRequest, ChangeListingLocationRequest, ChangeListingPriceRequest
from src.core.shared.presentation.dto import CurrentVendor
from src.core.shared.presentation.security import get_current_vendor

listing_router = APIRouter(prefix="/listing", tags=["Listing"])


@listing_router.post("/")
@inject
async def create_listing(
    dto: CreateListingRequest,
    usecase: Annotated[
        CreateListingUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.create_listing_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor)
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Listing created successfully"}


@listing_router.patch("/{listing_id}/price")
@inject
async def change_listing_price(
    listing_id: UUID,
    dto: ChangeListingPriceRequest,
    usecase: Annotated[
        ChangeListingPriceUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.change_listing_price_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor)
):
    await usecase.execute(listing_id, dto)
    return {"message": "Listing price changed successfully"}


@listing_router.patch("/{listing_id}/location")
@inject
async def change_listing_location(
    listing_id: UUID,
    dto: ChangeListingLocationRequest,
    usecase: Annotated[
        ChangeListingLocationUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.change_listing_location_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor)
):
    await usecase.execute(listing_id, dto)
    return {"message": "Listing location changed successfully"}


@listing_router.patch("/{listing_id}/description")
@inject
async def change_listing_description(
    listing_id: UUID,
    dto: ChangeListingDescriptionRequest,
    usecase: Annotated[
        ChangeListingDescriptionUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.change_listing_description_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor)
):
    await usecase.execute(listing_id, dto)
    return {"message": "Listing description changed successfully"}


@listing_router.patch("/{listing_id}/attributes")
@inject
async def change_listing_attribute(
    listing_id: UUID,
    dto: ChangeListingAttributeRequest,
    usecase: Annotated[
        ChangeListingAttributeUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.change_listing_attribute_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor)
):
    await usecase.execute(listing_id, dto)
    return {"message": "Listing attribute changed successfully"}


