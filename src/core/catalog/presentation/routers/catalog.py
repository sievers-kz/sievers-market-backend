from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter

from src.core.catalog.presentation.dependencies import CatalogQueryServiceDependency
from src.core.catalog.presentation.documentation import (
    GET_CATEGORY_TREE_DOC,
    GET_SUBCATEGORY_FILTERS_DOC,
    GET_SUBCATEGORY_FORM_DOC,
)
from src.core.catalog.presentation.dto.catalog import (
    AttributeResponse,
    FilterableAttributeResponse,
    RubricResponse,
)
from src.core.catalog.presentation.routers.attributes import attributes_router
from src.core.catalog.presentation.routers.categories import categories_router

catalog_router = APIRouter(prefix="/api/v1/catalog")
catalog_router.include_router(categories_router)
catalog_router.include_router(attributes_router)


@catalog_router.get(
    "/{subcategory_id}/form",
    response_model=AttributeResponse,
    operation_id=GET_SUBCATEGORY_FORM_DOC.operation_id,
    summary=GET_SUBCATEGORY_FORM_DOC.summary,
    responses=GET_SUBCATEGORY_FORM_DOC.responses_doc,
    description=GET_SUBCATEGORY_FORM_DOC.description,
)
@inject
async def get_form(
    subcategory_id: UUID,
    service: CatalogQueryServiceDependency,
):
    return await service.get_subcategory_attributes(subcategory_id)


@catalog_router.get(
    "/{subcategory_id}/filters",
    response_model=FilterableAttributeResponse,
    operation_id=GET_SUBCATEGORY_FILTERS_DOC.operation_id,
    summary=GET_SUBCATEGORY_FILTERS_DOC.summary,
    responses=GET_SUBCATEGORY_FILTERS_DOC.responses_doc,
    description=GET_SUBCATEGORY_FILTERS_DOC.description,
)
@inject
async def get_filters(
    subcategory_id: UUID,
    service: CatalogQueryServiceDependency,
):
    return await service.get_filterable_attributes(subcategory_id)


@catalog_router.get(
    "/tree",
    response_model=list[RubricResponse],
    operation_id=GET_CATEGORY_TREE_DOC.operation_id,
    summary=GET_CATEGORY_TREE_DOC.summary,
    responses=GET_CATEGORY_TREE_DOC.responses_doc,
    description=GET_CATEGORY_TREE_DOC.description,
)
@inject
async def get_category_tree(
    service: CatalogQueryServiceDependency,
):
    return await service.get_category_tree()
