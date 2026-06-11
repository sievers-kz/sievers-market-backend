from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security

from src.configuration.dependencies.container import ApplicationContainer
from src.core.listing.application.usecases import CreateListingUseCase, ChangeListingAttributeUseCase, \
    ChangeListingPriceUseCase, ChangeListingLocationUseCase, ChangeListingDescriptionUseCase, ActivateListingUseCase, \
    DeactivateListingUseCase, ArchiveListingUseCase, DeleteListingUseCase
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
    respone = await usecase.execute(current_vendor.id, dto)
    return {"message": "Listing created successfully", "response": respone}


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


@listing_router.patch("/{listing_id}/activate")
@inject
async def activate_listing(
    listing_id: UUID,
    usecase: Annotated[
        ActivateListingUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.activate_listing_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление активировано"}


@listing_router.patch("/{listing_id}/deactivate")
@inject
async def deactivate_listing(
    listing_id: UUID,
    usecase: Annotated[
        DeactivateListingUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.deactivate_listing_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление деактивировано"}


@listing_router.patch("/{listing_id}/archive")
@inject
async def archive_listing(
    listing_id: UUID,
    usecase: Annotated[
        ArchiveListingUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.archive_listing_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление архивировано"}


@listing_router.patch("/{listing_id}/delete")
@inject
async def delete_listing(
    listing_id: UUID,
    usecase: Annotated[
        DeleteListingUseCase,
        Depends(
            Provide[
                ApplicationContainer.listing.delete_listing_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление удалено"}