from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security, Query

from src.configuration.dependencies.container import ApplicationContainer
from src.core.listing.domain.enums import ListingStatus
from src.core.shared.presentation.dto import CurrentUser, CurrentVendor, PaginatedResponse
from src.core.shared.presentation.security import get_current_user, get_current_vendor

from src.core.vendor.application.services.vendor_validation import TaxpayerValidationService
from src.core.vendor.application.usecases import (
    RegisterVendorUseCase,
    ChangeContactFullnameUseCase,
    ChangeContactPhoneUseCase,
    ChangeShopNameUseCase,
    ChangeLogotypeUseCase, CloseVendorUseCase, RestoreVendorUseCase
)
from src.core.vendor.infrastructure.query import VendorCabinetQueryService

from src.core.vendor.presentation.dto import (
    CreateVendorRequest,
    TaxpayerResponse,
    ChangeContactFullnameRequest,
    ChangeContactPhoneRequest,
    ChangeShopNameRequest,
    ChangeLogotypeRequest, VendorProfileResponse, VendorListingCardsResponse
)


vendor_router = APIRouter(prefix="/vendor", tags=["Vendor"])


@vendor_router.get("/taxpayer/{tax_id}", response_model=TaxpayerResponse)
@inject
async def verify_vendor(
    tax_id: str,
    service: Annotated[
        TaxpayerValidationService,
        Depends(
            Provide[
                ApplicationContainer.vendor.taxpayer_validation_service
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    return await service.validate(tax_id)


@vendor_router.post("/", summary="Create a new vendor")
@inject
async def create_vendor(
    dto: CreateVendorRequest,
    usecase: Annotated[
        RegisterVendorUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.register_vendor_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Vendor successfully created"}


@vendor_router.patch("/contact-fullname", summary="Change contact fullname")
@inject
async def change_contact_fullname(
    dto: ChangeContactFullnameRequest,
    usecase: Annotated[
        ChangeContactFullnameUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.change_contact_fullname_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Contact fullname successfully changed"}


@vendor_router.patch("/contact-phone", summary="Change contact phone")
@inject
async def change_contact_phone(
    dto: ChangeContactPhoneRequest,
    usecase: Annotated[
        ChangeContactPhoneUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.change_contact_phone_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Contact phone successfully changed"}


@vendor_router.patch("/shop-name", summary="Change shop name")
@inject
async def change_shop_name(
    dto: ChangeShopNameRequest,
    usecase: Annotated[
        ChangeShopNameUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.change_shop_name_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Shop name successfully changed"}


@vendor_router.patch("/logotype", summary="Change logotype")
@inject
async def change_logotype(
    dto: ChangeLogotypeRequest,
    usecase: Annotated[
        ChangeLogotypeUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.change_logotype_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Logotype successfully changed"}


@vendor_router.get("/me", response_model=VendorProfileResponse)
@inject
async def get_me(
    service: Annotated[
        VendorCabinetQueryService,
        Depends(
            Provide[
                ApplicationContainer.vendor.vendor_cabinet_query_service
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    return await service.get_me(current_vendor.id)


@vendor_router.get("/me/listings/{status}", response_model=PaginatedResponse[VendorListingCardsResponse])
@inject
async def get_me_listings(
    status: ListingStatus,
    service: Annotated[
        VendorCabinetQueryService,
        Depends(
            Provide[
                ApplicationContainer.vendor.vendor_cabinet_query_service
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
    page: int = Query(1, alias="page"),
    limit: int = Query(10, alias="limit"),
):
    return await service.get_vendor_listing_cards_by_status(current_vendor.id, status, page, limit)


@vendor_router.patch("/close", summary="Close vendor profile")
@inject
async def close_vendor(
    usecase: Annotated[
        CloseVendorUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.close_vendor_usecase
            ]
        )
    ],
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id)
    return {"message": "Аккаунт продавца закрыт"}


@vendor_router.patch("/restore", summary="Restore vendor profile")
@inject
async def restore_vendor(
    usecase: Annotated[
        RestoreVendorUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.restore_vendor_usecase
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id)
    return {"message": "Аккаунт продавца восстановлен"}
