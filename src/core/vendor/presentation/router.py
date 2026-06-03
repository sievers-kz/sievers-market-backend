from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends, Security

from src.configuration.dependencies.container import ApplicationContainer
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

from src.core.vendor.application.services.vendor_validation import VendorValidationService
from src.core.vendor.application.usecases import (
    CreateVendorUseCase,
    ChangeContactFullnameUseCase,
    ChangeContactPhoneUseCase,
    ChangeShopNameUseCase,
    ChangeLogotypeUseCase
)
from src.core.vendor.infrastructure.query import VendorQueryService

from src.core.vendor.presentation.dto import (
    CreateVendorRequest,
    VendorValidationResponse,
    ChangeContactFullnameRequest,
    ChangeContactPhoneRequest,
    ChangeShopNameRequest,
    ChangeLogotypeRequest, VendorProfileResponse
)


vendor_router = APIRouter(prefix="/vendor", tags=["Vendor"])


@vendor_router.get("/verify/{tax_id}", response_model=VendorValidationResponse)
@inject
async def verify_vendor(
    tax_id: str,
    service: Annotated[
        VendorValidationService,
        Depends(
            Provide[
                ApplicationContainer.vendor.vendor_validation_service
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user)
):
    return await service.verify(tax_id)


@vendor_router.post("/", summary="Create a new vendor")
@inject
async def create_vendor(
    dto: CreateVendorRequest,
    usecase: Annotated[
        CreateVendorUseCase,
        Depends(
            Provide[
                ApplicationContainer.vendor.create_vendor_usecase
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
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
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
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
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
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
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
    current_user: CurrentUser = Security(get_current_user)
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Logotype successfully changed"}


@vendor_router.get("/me", response_model=VendorProfileResponse)
@inject
async def get_me(
    service: Annotated[
        VendorQueryService,
        Depends(
            Provide[
                ApplicationContainer.vendor.query_service
            ]
        )
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    return await service.get_me(current_user.id)
