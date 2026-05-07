from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.references.application.services import BrandService
from src.core.references.presentation.dto.brand import BrandResponse, CreateBrandRequest, UpdateBrandRequest


brand_router = APIRouter(prefix="/brand")


@brand_router.get("/{brand_id}")
@inject
async def get_brand(
    brand_id: UUID,
    service: Annotated[
        BrandService,
        Depends(
            Provide[
                ApplicationContainer.reference.brand_service
            ]
        )
    ]
):
    return await service.get_brand_by_id(brand_id)


@brand_router.get("/", response_model=list[BrandResponse])
@inject
async def get_brand_list(
    service: Annotated[
        BrandService,
        Depends(
            Provide[
                ApplicationContainer.reference.brand_service
            ]
        )
    ],
):
    return await service.get_brand_list()


@brand_router.post("/")
@inject
async def create_brand(
    dto: CreateBrandRequest,
    service: Annotated[
        BrandService,
        Depends(
            Provide[
                ApplicationContainer.reference.brand_service
            ]
        )
    ]
):
    await service.create_brand(dto)


@brand_router.patch("/{brand_id}")
@inject
async def update_brand(
    brand_id: UUID,
    dto: UpdateBrandRequest,
    service: Annotated[
        BrandService,
        Depends(
            Provide[
                ApplicationContainer.reference.brand_service
            ]
        )
    ]
):
    await service.update_brand(brand_id, dto)


@brand_router.delete("/{brand_id}")
@inject
async def delete_brand(
    brand_id: UUID,
    service: Annotated[
        BrandService,
        Depends(
            Provide[
                ApplicationContainer.reference.brand_service
            ]
        )
    ]
):
    await service.delete_brand(brand_id)