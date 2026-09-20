from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

from src.core.admin.domain.entities import Admin
from src.core.catalog.presentation.dependencies import (
    AttributeDefinitionRepositoryDependency,
    AttributeGroupRepositoryDependency,
    SubcategoryAttributeRepositoryDependency,
)
from src.core.catalog.presentation.documentation import (
    CREATE_ATTRIBUTE_DEFINITION_DOC,
    CREATE_ATTRIBUTE_GROUP_DOC,
    CREATE_SUBCATEGORY_ATTRIBUTE_DOC,
    GET_ALL_ATTRIBUTE_DEFINITIONS_DOC,
    GET_ALL_ATTRIBUTE_GROUPS_DOC,
)
from src.core.catalog.presentation.dto.attributes import (
    AttachAttributeRequest,
    AttributeDefinitionResponse,
    AttributeGroupResponse,
    CreateAttributeDefinitionRequest,
    CreateAttributeGroupRequest,
    SubcategoryAttributeResponse,
)
from src.core.shared.presentation.security import require_admin

attributes_router = APIRouter(tags=["Catalog Configuration"])


# =============================================================================
# ATTRIBUTE GROUPS
# =============================================================================


@attributes_router.post(
    "/attribute-group/",
    response_model=AttributeGroupResponse,
    operation_id=CREATE_ATTRIBUTE_GROUP_DOC.operation_id,
    summary=CREATE_ATTRIBUTE_GROUP_DOC.summary,
    responses=CREATE_ATTRIBUTE_GROUP_DOC.responses_doc,
    description=CREATE_ATTRIBUTE_GROUP_DOC.description,
)
@inject
async def create_attribute_group(
    dto: CreateAttributeGroupRequest,
    repository: AttributeGroupRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:attribute:group")),
):
    group = await repository.create(key=dto.key, label=dto.label, position=dto.position)
    return group


@attributes_router.get(
    "/attribute-group/",
    response_model=list[AttributeGroupResponse],
    operation_id=GET_ALL_ATTRIBUTE_GROUPS_DOC.operation_id,
    summary=GET_ALL_ATTRIBUTE_GROUPS_DOC.summary,
    responses=GET_ALL_ATTRIBUTE_GROUPS_DOC.responses_doc,
    description=GET_ALL_ATTRIBUTE_GROUPS_DOC.description,
)
@inject
async def get_all_attribute_groups(
    repository: AttributeGroupRepositoryDependency,
):
    return await repository.get_all()


# =============================================================================
# ATTRIBUTE DEFINITIONS
# =============================================================================


@attributes_router.post(
    "/attribute-definition/",
    response_model=AttributeDefinitionResponse,
    operation_id=CREATE_ATTRIBUTE_DEFINITION_DOC.operation_id,
    summary=CREATE_ATTRIBUTE_DEFINITION_DOC.summary,
    responses=CREATE_ATTRIBUTE_DEFINITION_DOC.responses_doc,
    description=CREATE_ATTRIBUTE_DEFINITION_DOC.description,
)
@inject
async def create_attribute_definition(
    dto: CreateAttributeDefinitionRequest,
    repository: AttributeDefinitionRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:attribute:definition")),
):
    definition = await repository.create(
        key=dto.key,
        label=dto.label,
        type=dto.type,
        options=[opt.model_dump() for opt in dto.options],
        source=dto.source,
    )
    return definition


@attributes_router.get(
    "/attribute-definition/",
    response_model=list[AttributeDefinitionResponse],
    operation_id=GET_ALL_ATTRIBUTE_DEFINITIONS_DOC.operation_id,
    summary=GET_ALL_ATTRIBUTE_DEFINITIONS_DOC.summary,
    responses=GET_ALL_ATTRIBUTE_DEFINITIONS_DOC.responses_doc,
    description=GET_ALL_ATTRIBUTE_DEFINITIONS_DOC.description,
)
@inject
async def get_all_attribute_definitions(
    repository: AttributeDefinitionRepositoryDependency,
):
    return await repository.get_all()


# =============================================================================
# SUBCATEGORY ATTRIBUTES (EAV Binding)
# =============================================================================


@attributes_router.post(
    "/subcategory-attribute/",
    response_model=SubcategoryAttributeResponse,
    operation_id=CREATE_SUBCATEGORY_ATTRIBUTE_DOC.operation_id,
    summary=CREATE_SUBCATEGORY_ATTRIBUTE_DOC.summary,
    responses=CREATE_SUBCATEGORY_ATTRIBUTE_DOC.responses_doc,
    description=CREATE_SUBCATEGORY_ATTRIBUTE_DOC.description,
)
@inject
async def create_subcategory_attribute(
    dto: AttachAttributeRequest,
    repository: SubcategoryAttributeRepositoryDependency,
    current_admin: Admin = Depends(require_admin("create:subcategory:attribute")),
):
    subcategory_attribute = await repository.create(
        subcategory_id=dto.subcategory_id,
        attribute_id=dto.attribute_id,
        group_id=dto.group_id,
        unit_id=dto.unit_id,
        required=dto.required,
        filterable=dto.filterable,
        position=dto.position,
    )
    return subcategory_attribute
