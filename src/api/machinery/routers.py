from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request
from fastapi.params import Depends, Security, Query

from src.api.machinery.dto import CreateMachinery, UpdateMachinery, PaginatedMachinery, DetailMachinery
from src.api.shared.dto import CurrentSeller
from src.api.shared.security import get_current_seller
from src.configuration.dependencies.container import ApplicationContainer

from src.core.machinery.application.usecases import (
    CreateMachineryUseCase,
    UpdateMachineryUseCase,
    ActivateMachineryUseCase,
    DeactivateMachineryUseCase,
    DeleteMachineryUseCase,
    FilterMachineryUseCase, GetSellerMachineryUseCase, GetDetailMachineryUseCase, GetOwnerDetailMachineryUseCase
)
from src.core.machinery.domain.enums import ListingStatus

machinery = APIRouter(prefix="/api/v1/machinery", tags=["Machinery"])


@machinery.post("/create")
@inject
async def create_active_machinery(
    dto: CreateMachinery,
    usecase: Annotated[
        CreateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.create_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    await usecase.execute(dto, current_seller.id)
    return {"message": "Listing created successfully"}


@machinery.patch("/{machinery_id}/update")
@inject
async def update_machinery(
    machinery_id: UUID,
    dto: UpdateMachinery,
    usecase: Annotated[
        UpdateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.update_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Listing updated successfully"}


@machinery.patch("/{machinery_id}/activate")
@inject
async def activate_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        ActivateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.activate_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    await usecase.execute(machinery_id)
    return {"message": "Listing activated successfully"}


@machinery.patch("/{machinery_id}/deactivate")
@inject
async def deactivate_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        DeactivateMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.deactivate_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    await usecase.execute(machinery_id)
    return {"message": "Listing deactivated successfully"}


@machinery.patch("/{machinery_id}/delete")
@inject
async def delete_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        DeleteMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.delete_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    await usecase.execute(machinery_id)
    return {"message": "Listing deleted successfully"}


@machinery.get("/", response_model=PaginatedMachinery)
@inject
async def filter_machinery(
    usecase: Annotated[
        FilterMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.filter_machinery_usecase
            ]
        )
    ],
    request: Request,
    category_id: UUID = Query(default=None, alias="category_id"),
    subcategory_id: UUID = Query(default=None, alias="subcategory_id"),
    min_price: int = Query(default=None, alias="min_price"),
    max_price: int = Query(default=None, alias="max_price"),
    city_id: UUID = Query(default=None, alias="city_id"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1)
):
    dynamic_filters = dict(request.query_params)
    return await usecase.execute(
        category_id=category_id,
        subcategory_id=subcategory_id,
        min_price=min_price,
        max_price=max_price,
        city_id=city_id,
        dynamic_filters=dynamic_filters,
        page=page,
        limit=limit
    )


@machinery.get("/me/{status}", response_model=PaginatedMachinery)
@inject
async def get_seller_machinery(
    status: ListingStatus,
    usecase: Annotated[
        GetSellerMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_seller_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1)
):
    return await usecase.execute(current_seller.id, status, page, limit)


@machinery.get("/{machinery_id}", response_model=DetailMachinery)
@inject
async def get_detail_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        GetDetailMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_detail_machinery_usecase
            ]
        )
    ],
):
    return await usecase.execute(machinery_id)


@machinery.get("/me/{machinery_id}/detail")
@inject
async def get_owner_detail_machinery(
    machinery_id: UUID,
    usecase: Annotated[
        GetOwnerDetailMachineryUseCase,
        Depends(
            Provide[
                ApplicationContainer.machinery.get_owner_detail_machinery_usecase
            ]
        )
    ],
    current_seller: CurrentSeller = Security(get_current_seller)
):
    return await usecase.execute(machinery_id, current_seller.id)