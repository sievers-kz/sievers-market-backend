from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.catalog.application.services.subcategory import SubcategoryService
from src.core.catalog.presentation.dto.subcategory import (
    ChangeSubcategoryNameRequest,
    ChangeSubcategoryParentRequest,
    CreateSubcategoryRequest,
    ReplaceSubcategoryAttributeRequest,
)

subcategory_router = APIRouter(prefix="/subcategory")


@subcategory_router.post("/", summary="Create a new subcategory")
@inject
async def create_subcategory(
    dto: CreateSubcategoryRequest,
    service: Annotated[
        SubcategoryService,
        Depends(Provide[ApplicationContainer.catalog.subcategory_service]),
    ],
):
    await service.create(dto)
    return {"message": "Subcategory created successfully"}


@subcategory_router.patch("/{subcategory_id}/parent")
@inject
async def change_subcategory_parent(
    subcategory_id: UUID,
    dto: ChangeSubcategoryParentRequest,
    service: Annotated[
        SubcategoryService,
        Depends(Provide[ApplicationContainer.catalog.subcategory_service]),
    ],
):
    await service.change_category(subcategory_id, dto)
    return {"message": "Subcategory parent updated successfully"}


@subcategory_router.patch("/{subcategory_id}/name")
@inject
async def change_subcategory_name(
    subcategory_id: UUID,
    dto: ChangeSubcategoryNameRequest,
    service: Annotated[
        SubcategoryService,
        Depends(Provide[ApplicationContainer.catalog.subcategory_service]),
    ],
):
    await service.change_name(subcategory_id, dto)
    return {"message": "Subcategory name updated successfully"}


@subcategory_router.patch("/{subcategory_id}/attributes")
@inject
async def change_subcategory_attributes(
    subcategory_id: UUID,
    dto: ReplaceSubcategoryAttributeRequest,
    service: Annotated[
        SubcategoryService,
        Depends(Provide[ApplicationContainer.catalog.subcategory_service]),
    ],
):
    await service.replace_attributes(subcategory_id, dto)
    return {"message": "Subcategory attributes updated successfully"}


@subcategory_router.delete("/{subcategory_id}")
@inject
async def delete_subcategory(
    subcategory_id: UUID,
    service: Annotated[
        SubcategoryService,
        Depends(Provide[ApplicationContainer.catalog.subcategory_service]),
    ],
):
    await service.delete_subcategory(subcategory_id)
    return {"message": "Subcategory deleted successfully"}
