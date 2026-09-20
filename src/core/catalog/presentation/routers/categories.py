from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

from src.core.admin.domain.entities import Admin
from src.core.catalog.infrastructure.enums import CatalogStatus
from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.catalog.presentation.dependencies import (
    CategoryRepositoryDependency,
    RubricRepositoryDependency,
    SubcategoryRepositoryDependency,
)
from src.core.catalog.presentation.documentation import (
    CHANGE_CATEGORY_NAME_DOC,
    CHANGE_CATEGORY_PARENT_DOC,
    CHANGE_RUBRIC_NAME_DOC,
    CHANGE_SUBCATEGORY_NAME_DOC,
    CHANGE_SUBCATEGORY_PARENT_DOC,
    CREATE_CATEGORY_DOC,
    CREATE_RUBRIC_DOC,
    CREATE_SUBCATEGORY_DOC,
    DELETE_CATEGORY_DOC,
    DELETE_RUBRIC_DOC,
    DELETE_SUBCATEGORY_DOC,
)
from src.core.catalog.presentation.dto.category import (
    ChangeCategoryNameRequest,
    ChangeCategoryParentRequest,
    CreateCategoryRequest,
)
from src.core.catalog.presentation.dto.rubric import (
    ChangeRubricNameRequest,
    CreateRubricRequest,
)
from src.core.catalog.presentation.dto.subcategory import (
    ChangeSubcategoryNameRequest,
    ChangeSubcategoryParentRequest,
    CreateSubcategoryRequest,
)
from src.core.shared.presentation.security import require_admin

categories_router = APIRouter(tags=["Catalog Categories"])


# =============================================================================
# RUBRICS
# =============================================================================


@categories_router.post(
    "/rubric/",
    operation_id=CREATE_RUBRIC_DOC.operation_id,
    summary=CREATE_RUBRIC_DOC.summary,
    responses=CREATE_RUBRIC_DOC.responses_doc,
    description=CREATE_RUBRIC_DOC.description,
)
@inject
async def create_rubric(
    dto: CreateRubricRequest,
    rubric_repo: RubricRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:rubric")),
):
    rubric = await rubric_repo.create(name=dto.name)
    return {"message": "Rubric created successfully", "id": rubric.id}


@categories_router.patch(
    "/rubric/{rubric_id}/name",
    operation_id=CHANGE_RUBRIC_NAME_DOC.operation_id,
    summary=CHANGE_RUBRIC_NAME_DOC.summary,
    responses=CHANGE_RUBRIC_NAME_DOC.responses_doc,
    description=CHANGE_RUBRIC_NAME_DOC.description,
)
@inject
async def change_rubric_name(
    rubric_id: UUID,
    dto: ChangeRubricNameRequest,
    rubric_repo: RubricRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:rubric")),
):
    rubric = await rubric_repo.get_by_id(rubric_id)
    if not rubric:
        raise CatalogNotFoundError(field=str(rubric_id))

    rubric.name = dto.name
    await rubric_repo.save(rubric)
    return {"message": "Rubric name updated successfully"}


@categories_router.delete(
    "/rubric/{rubric_id}",
    operation_id=DELETE_RUBRIC_DOC.operation_id,
    summary=DELETE_RUBRIC_DOC.summary,
    responses=DELETE_RUBRIC_DOC.responses_doc,
    description=DELETE_RUBRIC_DOC.description,
)
@inject
async def delete_rubric(
    rubric_id: UUID,
    rubric_repo: RubricRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:rubric")),
):
    rubric = await rubric_repo.get_by_id(rubric_id)
    if not rubric:
        raise CatalogNotFoundError(field=str(rubric_id))

    rubric.status = CatalogStatus.DELETED
    await rubric_repo.save(rubric)
    return {"message": "Rubric deleted successfully"}


# =============================================================================
# CATEGORIES
# =============================================================================


@categories_router.post(
    "/category/",
    operation_id=CREATE_CATEGORY_DOC.operation_id,
    summary=CREATE_CATEGORY_DOC.summary,
    responses=CREATE_CATEGORY_DOC.responses_doc,
    description=CREATE_CATEGORY_DOC.description,
)
@inject
async def create_category(
    dto: CreateCategoryRequest,
    category_repo: CategoryRepositoryDependency,
    rubric_repo: RubricRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:category")),
):
    rubric = await rubric_repo.get_by_id(dto.rubric_id)
    if not rubric:
        raise CatalogNotFoundError(field=str(dto.rubric_id))

    category = await category_repo.create(rubric_id=dto.rubric_id, name=dto.name)
    return {"message": "Category created successfully", "id": category.id}


@categories_router.patch(
    "/category/{category_id}/parent",
    operation_id=CHANGE_CATEGORY_PARENT_DOC.operation_id,
    summary=CHANGE_CATEGORY_PARENT_DOC.summary,
    responses=CHANGE_CATEGORY_PARENT_DOC.responses_doc,
    description=CHANGE_CATEGORY_PARENT_DOC.description,
)
@inject
async def change_category_parent(
    category_id: UUID,
    dto: ChangeCategoryParentRequest,
    category_repo: CategoryRepositoryDependency,
    rubric_repo: RubricRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:category")),
):
    rubric = await rubric_repo.get_by_id(dto.rubric_id)
    if not rubric:
        raise CatalogNotFoundError(field=str(dto.rubric_id))

    category = await category_repo.get_by_id(category_id)
    if not category:
        raise CatalogNotFoundError(field=str(category_id))

    category.rubric_id = dto.rubric_id
    await category_repo.save(category)
    return {"message": "Category parent updated successfully"}


@categories_router.patch(
    "/category/{category_id}/name",
    operation_id=CHANGE_CATEGORY_NAME_DOC.operation_id,
    summary=CHANGE_CATEGORY_NAME_DOC.summary,
    responses=CHANGE_CATEGORY_NAME_DOC.responses_doc,
    description=CHANGE_CATEGORY_NAME_DOC.description,
)
@inject
async def change_category_name(
    category_id: UUID,
    dto: ChangeCategoryNameRequest,
    category_repo: CategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:category")),
):
    category = await category_repo.get_by_id(category_id)
    if not category:
        raise CatalogNotFoundError(field=str(category_id))

    category.name = dto.name
    await category_repo.save(category)
    return {"message": "Category name updated successfully"}


@categories_router.delete(
    "/category/{category_id}",
    operation_id=DELETE_CATEGORY_DOC.operation_id,
    summary=DELETE_CATEGORY_DOC.summary,
    responses=DELETE_CATEGORY_DOC.responses_doc,
    description=DELETE_CATEGORY_DOC.description,
)
@inject
async def delete_category(
    category_id: UUID,
    category_repo: CategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:category")),
):
    category = await category_repo.get_by_id(category_id)
    if not category:
        raise CatalogNotFoundError(field=str(category_id))

    category.status = CatalogStatus.DELETED
    await category_repo.save(category)
    return {"message": "Category deleted successfully"}


# =============================================================================
# SUBCATEGORIES
# =============================================================================


@categories_router.post(
    "/subcategory/",
    operation_id=CREATE_SUBCATEGORY_DOC.operation_id,
    summary=CREATE_SUBCATEGORY_DOC.summary,
    responses=CREATE_SUBCATEGORY_DOC.responses_doc,
    description=CREATE_SUBCATEGORY_DOC.description,
)
@inject
async def create_subcategory(
    dto: CreateSubcategoryRequest,
    subcategory_repo: SubcategoryRepositoryDependency,
    category_repo: CategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:subcategory")),
):
    category = await category_repo.get_by_id(dto.category_id)
    if not category:
        raise CatalogNotFoundError(field=str(dto.category_id))

    subcategory = await subcategory_repo.create(category_id=dto.category_id, name=dto.name)
    return {"message": "Subcategory created successfully", "id": subcategory.id}


@categories_router.patch(
    "/subcategory/{subcategory_id}/parent",
    operation_id=CHANGE_SUBCATEGORY_PARENT_DOC.operation_id,
    summary=CHANGE_SUBCATEGORY_PARENT_DOC.summary,
    responses=CHANGE_SUBCATEGORY_PARENT_DOC.responses_doc,
    description=CHANGE_SUBCATEGORY_PARENT_DOC.description,
)
@inject
async def change_subcategory_parent(
    subcategory_id: UUID,
    dto: ChangeSubcategoryParentRequest,
    subcategory_repo: SubcategoryRepositoryDependency,
    category_repo: CategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:subcategory")),
):
    category = await category_repo.get_by_id(dto.category_id)
    if not category:
        raise CatalogNotFoundError(field=str(dto.category_id))

    subcategory = await subcategory_repo.get_by_id(subcategory_id)
    if not subcategory:
        raise CatalogNotFoundError(field=str(subcategory_id))

    subcategory.category_id = dto.category_id
    await subcategory_repo.save(subcategory)
    return {"message": "Subcategory parent updated successfully"}


@categories_router.patch(
    "/subcategory/{subcategory_id}/name",
    operation_id=CHANGE_SUBCATEGORY_NAME_DOC.operation_id,
    summary=CHANGE_SUBCATEGORY_NAME_DOC.summary,
    responses=CHANGE_SUBCATEGORY_NAME_DOC.responses_doc,
    description=CHANGE_SUBCATEGORY_NAME_DOC.description,
)
@inject
async def change_subcategory_name(
    subcategory_id: UUID,
    dto: ChangeSubcategoryNameRequest,
    subcategory_repo: SubcategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("update:subcategory")),
):
    subcategory = await subcategory_repo.get_by_id(subcategory_id)
    if not subcategory:
        raise CatalogNotFoundError(field=str(subcategory_id))

    subcategory.name = dto.name
    await subcategory_repo.save(subcategory)
    return {"message": "Subcategory name updated successfully"}


@categories_router.delete(
    "/subcategory/{subcategory_id}",
    operation_id=DELETE_SUBCATEGORY_DOC.operation_id,
    summary=DELETE_SUBCATEGORY_DOC.summary,
    responses=DELETE_SUBCATEGORY_DOC.responses_doc,
    description=DELETE_SUBCATEGORY_DOC.description,
)
@inject
async def delete_subcategory(
    subcategory_id: UUID,
    subcategory_repo: SubcategoryRepositoryDependency,
    current_admin: Admin = Depends(require_admin("delete:subcategory")),
):
    subcategory = await subcategory_repo.get_by_id(subcategory_id)
    if not subcategory:
        raise CatalogNotFoundError(field=str(subcategory_id))

    subcategory.status = CatalogStatus.DELETED
    await subcategory_repo.save(subcategory)
    return {"message": "Subcategory deleted successfully"}
