from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.admin.domain.entities import Admin
from src.core.references.presentation.dependencies import ColorRepositoryDependency
from src.core.references.presentation.documentation import (
    CREATE_COLOR_DOC,
    DELETE_COLOR_DOC,
    GET_ALL_COLORS_DOC,
    GET_COLOR_BY_ID_DOC,
    UPDATE_COLOR_DOC,
)
from src.core.references.presentation.dto.color import (
    ColorResponse,
    CreateColorRequest,
    UpdateColorRequest,
)
from src.core.shared.presentation.security import require_admin

color_router = APIRouter(prefix="/color", tags=["Color Reference"])


@color_router.get(
    "/",
    response_model=list[ColorResponse],
    operation_id=GET_ALL_COLORS_DOC.operation_id,
    summary=GET_ALL_COLORS_DOC.summary,
    responses=GET_ALL_COLORS_DOC.responses_doc,
    description=GET_ALL_COLORS_DOC.description,
)
@inject
async def get_all(repository: ColorRepositoryDependency):
    return await repository.get_all()


@color_router.get(
    "/{color_id}",
    response_model=ColorResponse,
    operation_id=GET_COLOR_BY_ID_DOC.operation_id,
    summary=GET_COLOR_BY_ID_DOC.summary,
    responses=GET_COLOR_BY_ID_DOC.responses_doc,
    description=GET_COLOR_BY_ID_DOC.description,
)
@inject
async def get_by_id(color_id: UUID, repository: ColorRepositoryDependency):
    color = await repository.get_by_id(color_id)
    if not color:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден")
    return color


@color_router.post(
    "/",
    response_model=ColorResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id=CREATE_COLOR_DOC.operation_id,
    summary=CREATE_COLOR_DOC.summary,
    responses=CREATE_COLOR_DOC.responses_doc,
    description=CREATE_COLOR_DOC.description,
)
async def create(
    dto: CreateColorRequest,
    repository: ColorRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:color")),
):
    return await repository.create(**dto.model_dump())


@color_router.patch(
    "/{color_id}",
    response_model=ColorResponse,
    operation_id=UPDATE_COLOR_DOC.operation_id,
    summary=UPDATE_COLOR_DOC.summary,
    responses=UPDATE_COLOR_DOC.responses_doc,
    description=UPDATE_COLOR_DOC.description,
)
async def update(
    color_id: UUID,
    dto: UpdateColorRequest,
    repository: ColorRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:color")),
):
    color = await repository.update(color_id, **dto.model_dump())
    if not color:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден")
    return color


@color_router.delete(
    "/{color_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id=DELETE_COLOR_DOC.operation_id,
    summary=DELETE_COLOR_DOC.summary,
    responses=DELETE_COLOR_DOC.responses_doc,
    description=DELETE_COLOR_DOC.description,
)
async def delete(
    color_id: UUID,
    repository: ColorRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:color")),
):
    deleted = await repository.delete(color_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Цвет не найден")
