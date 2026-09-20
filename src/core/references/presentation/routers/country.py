from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.admin.domain.entities import Admin
from src.core.references.presentation.dependencies import (
    OriginCountryRepositoryDependency,
)
from src.core.references.presentation.documentation import (
    CREATE_ORIGIN_COUNTRY_DOC,
    DELETE_ORIGIN_COUNTRY_DOC,
    GET_ALL_ORIGIN_COUNTRIES_DOC,
    GET_ORIGIN_COUNTRY_BY_ID_DOC,
    UPDATE_ORIGIN_COUNTRY_DOC,
)
from src.core.references.presentation.dto.country import (
    CreateOriginCountryRequest,
    OriginCountryResponse,
    UpdateOriginCountryRequest,
)
from src.core.shared.presentation.security import require_admin

origin_country_router = APIRouter(prefix="/country", tags=["Origin Country Reference"])


@origin_country_router.get(
    "/",
    response_model=list[OriginCountryResponse],
    operation_id=GET_ALL_ORIGIN_COUNTRIES_DOC.operation_id,
    summary=GET_ALL_ORIGIN_COUNTRIES_DOC.summary,
    responses=GET_ALL_ORIGIN_COUNTRIES_DOC.responses_doc,
    description=GET_ALL_ORIGIN_COUNTRIES_DOC.description,
)
@inject
async def get_all(repository: OriginCountryRepositoryDependency):
    return await repository.get_all()


@origin_country_router.get(
    "/{country_id}",
    response_model=OriginCountryResponse,
    operation_id=GET_ORIGIN_COUNTRY_BY_ID_DOC.operation_id,
    summary=GET_ORIGIN_COUNTRY_BY_ID_DOC.summary,
    responses=GET_ORIGIN_COUNTRY_BY_ID_DOC.responses_doc,
    description=GET_ORIGIN_COUNTRY_BY_ID_DOC.description,
)
@inject
async def get_by_id(country_id: UUID, repository: OriginCountryRepositoryDependency):
    country = await repository.get_by_id(country_id)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Страна не найдена")
    return country


@origin_country_router.post(
    "/",
    response_model=OriginCountryResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id=CREATE_ORIGIN_COUNTRY_DOC.operation_id,
    summary=CREATE_ORIGIN_COUNTRY_DOC.summary,
    responses=CREATE_ORIGIN_COUNTRY_DOC.responses_doc,
    description=CREATE_ORIGIN_COUNTRY_DOC.description,
)
async def create(
    dto: CreateOriginCountryRequest,
    repository: OriginCountryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:country")),
):
    return await repository.create(**dto.model_dump())


@origin_country_router.patch(
    "/{country_id}",
    response_model=OriginCountryResponse,
    operation_id=UPDATE_ORIGIN_COUNTRY_DOC.operation_id,
    summary=UPDATE_ORIGIN_COUNTRY_DOC.summary,
    responses=UPDATE_ORIGIN_COUNTRY_DOC.responses_doc,
    description=UPDATE_ORIGIN_COUNTRY_DOC.description,
)
async def update(
    country_id: UUID,
    dto: UpdateOriginCountryRequest,
    repository: OriginCountryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:country")),
):
    country = await repository.update(country_id, **dto.model_dump())
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Страна не найдена")
    return country


@origin_country_router.delete(
    "/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id=DELETE_ORIGIN_COUNTRY_DOC.operation_id,
    summary=DELETE_ORIGIN_COUNTRY_DOC.summary,
    responses=DELETE_ORIGIN_COUNTRY_DOC.responses_doc,
    description=DELETE_ORIGIN_COUNTRY_DOC.description,
)
async def delete(
    country_id: UUID,
    repository: OriginCountryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:country")),
):
    deleted = await repository.delete(country_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Страна не найдена")
