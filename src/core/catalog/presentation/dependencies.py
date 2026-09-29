from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.catalog.infrastructure.query import CatalogQueryService
from src.core.catalog.infrastructure.repositories.attributes import (
    AttributeDefinitionRepository,
    AttributeGroupRepository,
    SubcategoryAttributeRepository,
)
from src.core.catalog.infrastructure.repositories.categories import (
    CategoryRepository,
    RubricRepository,
    SubcategoryRepository,
)

CatalogQueryServiceDependency = Annotated[
    CatalogQueryService, Depends(Provide[ApplicationContainer.catalog.query_service])
]

# ================= Catalog Categories Dependencies =====================

RubricRepositoryDependency = Annotated[
    RubricRepository, Depends(Provide[ApplicationContainer.catalog.rubric_repository])
]

CategoryRepositoryDependency = Annotated[
    CategoryRepository,
    Depends(Provide[ApplicationContainer.catalog.category_repository]),
]

SubcategoryRepositoryDependency = Annotated[
    SubcategoryRepository,
    Depends(Provide[ApplicationContainer.catalog.subcategory_repository]),
]

# ================= Catalog Attributes Dependencies =====================

AttributeDefinitionRepositoryDependency = Annotated[
    AttributeDefinitionRepository,
    Depends(Provide[ApplicationContainer.catalog.attribute_definition_repository]),
]

AttributeGroupRepositoryDependency = Annotated[
    AttributeGroupRepository,
    Depends(Provide[ApplicationContainer.catalog.attribute_group_repository]),
]

SubcategoryAttributeRepositoryDependency = Annotated[
    SubcategoryAttributeRepository,
    Depends(Provide[ApplicationContainer.catalog.subcategory_attribute_repository]),
]
