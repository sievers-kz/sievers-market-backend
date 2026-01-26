from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from dependency_injector.wiring import inject, Provide

from src.api.media.dto import UploadMediaDTO, UpdateMediaDTO, MediaResponse, \
    BatchPresignedUrlResponse, BatchPresignedUrlRequest
from src.configuration.dependencies.container import ApplicationContainer
from src.core.media.application.usecases import GetPreSignedUrlsUseCase, UploadMediaUseCase, UpdateMediaUseCase, \
    GetMediaUseCase

media = APIRouter(prefix="/api/v1/media", tags=["Media"])


@media.post("/pre-signed-url/{filename}", response_model=BatchPresignedUrlResponse)
@inject
async def generate_presigned_url(
    dto: BatchPresignedUrlRequest,
    usecase: Annotated[
        GetPreSignedUrlsUseCase,
        Depends(
            Provide[
                ApplicationContainer.media.generate_presigned_url_usecase
            ]
        )
    ],
):
    return await usecase.execute(dto)


@media.post("/upload")
@inject
async def upload_media(
    dto: UploadMediaDTO,
    usecase: Annotated[
        UploadMediaUseCase,
        Depends(
            Provide[
                ApplicationContainer.media.upload_media_usecase
            ]
        )
    ]
):
    await usecase.execute(dto)
    return {"message": "Media uploaded successfully"}


@media.put("/update/{machinery_id}")
@inject
async def update_media(
    machinery_id: UUID,
    dto: UpdateMediaDTO,
    usecase: Annotated[
        UpdateMediaUseCase,
        Depends(
            Provide[
                ApplicationContainer.media.update_media_usecase
            ]
        )
    ]
):
    await usecase.execute(machinery_id, dto)
    return {"message": "Media updated successfully"}


@media.get("/{machinery_id}", response_model=list[MediaResponse])
@inject
async def get_media(
    machinery_id: UUID,
    usecase: Annotated[
        GetMediaUseCase,
        Depends(
            Provide[
                ApplicationContainer.media.get_media_usecase
            ]
        )
    ]
):
    return await usecase.execute(machinery_id)
