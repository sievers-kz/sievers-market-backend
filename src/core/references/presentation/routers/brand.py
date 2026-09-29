from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.admin.domain.entities import Admin
from src.core.references.presentation.dependencies import BrandRepositoryDependency
from src.core.references.presentation.documentation import (
    CREATE_BRAND_DOC,
    DELETE_BRAND_DOC,
    GET_ALL_BRANDS_DOC,
    GET_BRAND_BY_ID_DOC,
    UPDATE_BRAND_DOC,
)
from src.core.references.presentation.dto.brand import (
    BrandResponse,
    CreateBrandRequest,
    UpdateBrandRequest,
)
from src.core.shared.presentation.security import require_admin

brand_router = APIRouter(prefix="/brand", tags=["Brand Reference"])


@brand_router.get(
    "/",
    response_model=list[BrandResponse],
    operation_id=GET_ALL_BRANDS_DOC.operation_id,
    summary=GET_ALL_BRANDS_DOC.summary,
    responses=GET_ALL_BRANDS_DOC.responses_doc,
    description=GET_ALL_BRANDS_DOC.description,
)
@inject
async def get_all(repository: BrandRepositoryDependency):
    return await repository.get_all()


@brand_router.get(
    "/{brand_id}",
    response_model=BrandResponse,
    operation_id=GET_BRAND_BY_ID_DOC.operation_id,
    summary=GET_BRAND_BY_ID_DOC.summary,
    responses=GET_BRAND_BY_ID_DOC.responses_doc,
    description=GET_BRAND_BY_ID_DOC.description,
)
@inject
async def get_by_id(brand_id: UUID, repository: BrandRepositoryDependency):
    brand = await repository.get_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бренд не найден")
    return brand


@brand_router.post(
    "/",
    response_model=BrandResponse,
    operation_id=CREATE_BRAND_DOC.operation_id,
    summary=CREATE_BRAND_DOC.summary,
    responses=CREATE_BRAND_DOC.responses_doc,
    description=CREATE_BRAND_DOC.description,
)
@inject
async def create(
    dto: CreateBrandRequest,
    repository: BrandRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:brand")),
):
    return await repository.create(**dto.model_dump())


@brand_router.patch(
    "/{brand_id}",
    response_model=BrandResponse,
    operation_id=UPDATE_BRAND_DOC.operation_id,
    summary=UPDATE_BRAND_DOC.summary,
    responses=UPDATE_BRAND_DOC.responses_doc,
    description=UPDATE_BRAND_DOC.description,
)
@inject
async def update(
    brand_id: UUID,
    dto: UpdateBrandRequest,
    repository: BrandRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:brand")),
):
    brand = await repository.update(brand_id, **dto.model_dump())
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бренд не найден")
    return brand


@brand_router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id=DELETE_BRAND_DOC.operation_id,
    summary=DELETE_BRAND_DOC.summary,
    responses=DELETE_BRAND_DOC.responses_doc,
    description=DELETE_BRAND_DOC.description,
)
async def delete(
    brand_id: UUID,
    repository: BrandRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:brand")),
):
    deleted = await repository.delete(brand_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бренд не найден")
