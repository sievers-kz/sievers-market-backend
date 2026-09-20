from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Security
from fastapi.responses import RedirectResponse

from src.core.media.presentation.dependencies import MediaServiceDependency
from src.core.media.presentation.documentation import (
    CONFIRM_UPLOAD_DOC,
    GENERATE_UPLOAD_URL_DOC,
    GET_MEDIA_DOC,
)
from src.core.media.presentation.dto import (
    ConfirmUploadRequest,
    ConfirmUploadResponse,
    GenerateUploadUrlRequest,
    UploadUrlResponse,
)
from src.core.shared.presentation.dto import CurrentUser
from src.core.shared.presentation.security import get_current_user

media_router = APIRouter(prefix="/api/v1/media", tags=["Media"])


@media_router.post(
    "/url/upload",
    response_model=list[UploadUrlResponse],
    operation_id=GENERATE_UPLOAD_URL_DOC.operation_id,
    summary=GENERATE_UPLOAD_URL_DOC.summary,
    responses=GENERATE_UPLOAD_URL_DOC.responses_doc,
    description=GENERATE_UPLOAD_URL_DOC.description,
)
@inject
async def generate_upload_url(
    dto: GenerateUploadUrlRequest,
    service: MediaServiceDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    return await service.generate_upload_url(dto)


@media_router.post(
    "/upload/confirm",
    response_model=list[ConfirmUploadResponse],
    operation_id=CONFIRM_UPLOAD_DOC.operation_id,
    summary=CONFIRM_UPLOAD_DOC.summary,
    responses=CONFIRM_UPLOAD_DOC.responses_doc,
    description=CONFIRM_UPLOAD_DOC.description,
)
@inject
async def confirm_upload(
    dto: ConfirmUploadRequest,
    service: MediaServiceDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    media_response = await service.confirm_upload(current_user.id, dto)
    return media_response


@media_router.get(
    "/{media_id}",
    operation_id=GET_MEDIA_DOC.operation_id,
    summary=GET_MEDIA_DOC.summary,
    responses=GET_MEDIA_DOC.responses_doc,
    description=GET_MEDIA_DOC.description,
)
@inject
async def get_media(
    media_id: UUID,
    service: MediaServiceDependency,
):
    url = await service.get_media_url(media_id)
    return RedirectResponse(url)
