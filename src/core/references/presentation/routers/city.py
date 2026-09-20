from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.core.admin.domain.entities import Admin
from src.core.references.presentation.dependencies import CityRepositoryDependency
from src.core.references.presentation.documentation import (
    CREATE_CITY_DOC,
    DELETE_CITY_DOC,
    GET_ALL_CITIES_DOC,
    GET_CITY_BY_ID_DOC,
    UPDATE_CITY_DOC,
)
from src.core.references.presentation.dto.city import (
    CityResponse,
    CreateCityRequest,
    UpdateCityRequest,
)
from src.core.shared.presentation.security import require_admin

city_router = APIRouter(prefix="/city", tags=["City Reference"])


@city_router.get(
    "/",
    response_model=list[CityResponse],
    operation_id=GET_ALL_CITIES_DOC.operation_id,
    summary=GET_ALL_CITIES_DOC.summary,
    responses=GET_ALL_CITIES_DOC.responses_doc,
    description=GET_ALL_CITIES_DOC.description,
)
@inject
async def get_all(repository: CityRepositoryDependency):
    return await repository.get_all()


@city_router.get(
    "/{city_id}",
    response_model=CityResponse,
    operation_id=GET_CITY_BY_ID_DOC.operation_id,
    summary=GET_CITY_BY_ID_DOC.summary,
    responses=GET_CITY_BY_ID_DOC.responses_doc,
    description=GET_CITY_BY_ID_DOC.description,
)
@inject
async def get_by_id(city_id: UUID, repository: CityRepositoryDependency):
    city = await repository.get_by_id(city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Город не найден")
    return city


@city_router.post(
    "/",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id=CREATE_CITY_DOC.operation_id,
    summary=CREATE_CITY_DOC.summary,
    responses=CREATE_CITY_DOC.responses_doc,
    description=CREATE_CITY_DOC.description,
)
async def create(
    dto: CreateCityRequest,
    repository: CityRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:city")),
):
    return await repository.create(**dto.model_dump())


@city_router.patch(
    "/{city_id}",
    response_model=CityResponse,
    operation_id=UPDATE_CITY_DOC.operation_id,
    summary=UPDATE_CITY_DOC.summary,
    responses=UPDATE_CITY_DOC.responses_doc,
    description=UPDATE_CITY_DOC.description,
)
async def update(
    city_id: UUID,
    dto: UpdateCityRequest,
    repository: CityRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:city")),
):
    city = await repository.update(city_id, **dto.model_dump())
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Город не найден")
    return city


@city_router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id=DELETE_CITY_DOC.operation_id,
    summary=DELETE_CITY_DOC.summary,
    responses=DELETE_CITY_DOC.responses_doc,
    description=DELETE_CITY_DOC.description,
)
async def delete(
    city_id: UUID,
    repository: CityRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:city")),
):
    deleted = await repository.delete(city_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Город не найден")
