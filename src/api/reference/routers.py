from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.reference.dto import CountryDTO, RegionDTO, BrandDTO, FilterAttribute, FormField, ColorDTO
from src.configuration.dependencies.container import ApplicationContainer

from src.core.references.application.usecases import (
    GetSubcategoryFilterUseCase,
    GetSubcategoryFormUseCase,
    GetBrandsUseCase,
    GetRegionsUseCase,
    GetCountriesUseCase,
    GetColorsUseCase
)

reference = APIRouter(prefix="/api/v1/reference", tags=["References"])


@reference.get("/categories/{id}/filters", response_model=list[FilterAttribute])
@inject
async def get_subcategory_filter(
    id: UUID,
    usecase: Annotated[
        GetSubcategoryFilterUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_subcategory_filter_usecase
            ]
        )
    ]
):
    return await usecase.execute(id)


@reference.get("/category/{id}/form", response_model=list[FormField])
@inject
async def get_category_form(
    id: UUID,
    usecase: Annotated[
        GetSubcategoryFormUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_subcategory_form_usecase
            ]
        )
    ],
):
    return await usecase.execute(id)


@reference.get("/brands", response_model=list[BrandDTO])
@inject
async def get_all_brands(
    usecase: Annotated[
        GetBrandsUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_brands_usecase
            ]
        )
    ],
):
    return await usecase.execute()


@reference.get("/regions", response_model=list[RegionDTO])
@inject
async def get_all_regions(
    usecase: Annotated[
        GetRegionsUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_regions_usecase
            ]
        )
    ]
):
    return await usecase.execute()


@reference.get("/countries", response_model=list[CountryDTO])
@inject
async def get_all_countries(
    usecase: Annotated[
        GetCountriesUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_countries_usecase
            ]
        )
    ]
):
    return await usecase.execute()


@reference.get("/colors", response_model=list[ColorDTO])
@inject
async def get_all_colors(
    usecase: Annotated[
        GetColorsUseCase,
        Depends(
            Provide[
                ApplicationContainer.reference.get_colors_usecase
            ]
        )
    ]
):
    return await usecase.execute()
