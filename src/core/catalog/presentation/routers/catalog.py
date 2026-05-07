from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.catalog.infrastructure.query import CatalogQueryService
from src.core.catalog.presentation.dto.catalog import AttributeResponse, RubricResponse
from src.core.catalog.presentation.routers.subcategory import subcategory_router


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
