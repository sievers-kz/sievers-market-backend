from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.references.application.services import ColorService
from src.core.references.presentation.dto.color import ColorResponse, CreateColorRequest, UpdateColorRequest


color_router = APIRouter(prefix="/color")


@color_router.get("/{color_id}", response_model=ColorResponse)
@inject
async def get_color(
    color_id: UUID,
    service: Annotated[
        ColorService,
        Depends(
            Provide[
                ApplicationContainer.reference.color_service
            ]
        )
    ]
):
    return await service.get_color_by_id(color_id)


@color_router.get("/", response_model=list[ColorResponse])
@inject
async def get_color_list(
    service: Annotated[
        ColorService,
        Depends(
            Provide[
                ApplicationContainer.reference.color_service
            ]
        )
    ]
):
    return await service.get_color_list()


@color_router.post("/")
@inject
async def create_color(
    dto: CreateColorRequest,
    service: Annotated[
        ColorService,
        Depends(
            Provide[
                ApplicationContainer.reference.color_service
            ]
        )
    ]
):
    return await service.create_color(dto)


@color_router.patch("/{color_id}")
@inject
async def update_color(
    color_id: UUID,
    dto: UpdateColorRequest,
    service: Annotated[
        ColorService,
        Depends(
            Provide[
                ApplicationContainer.reference.color_service
            ]
        )
    ]
):
    await service.update_color(color_id, dto)


@color_router.delete("/{color_id}")
@inject
async def delete_color(
    color_id: UUID,
    service: Annotated[
        ColorService,
        Depends(
            Provide[
                ApplicationContainer.reference.color_service
            ]
        )
    ]
):
    await service.delete_color(color_id)
