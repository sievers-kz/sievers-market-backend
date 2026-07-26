from dependency_injector import containers, providers

from src.core.catalog.infrastructure.attribute_validation import (
    AttributeValidationService,
)
from src.core.catalog.infrastructure.query import CatalogQueryService
from src.core.catalog.infrastructure.repositories.attributes import (
    AttributeDefinitionRepository,
    AttributeGroupRepository,
    SubcategoryAttributeRepository,
    UnitOfMeasureRepository,
)
from src.core.catalog.infrastructure.repositories.categories import (
    CategoryRepository,
    RubricRepository,
    SubcategoryRepository,
)


class CatalogContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    rubric_repository = providers.Factory(RubricRepository, session=database_session)
    category_repository = providers.Factory(
        CategoryRepository, session=database_session
    )
    subcategory_repository = providers.Factory(
        SubcategoryRepository, session=database_session
    )

    attribute_definition_repository = providers.Factory(
        AttributeDefinitionRepository, session=database_session
    )
    subcategory_attribute_repository = providers.Factory(
        SubcategoryAttributeRepository, session=database_session
    )
    attribute_group_repository = providers.Factory(
        AttributeGroupRepository, session=database_session
    )
    unit_of_measure_repository = providers.Factory(
        UnitOfMeasureRepository, session=database_session
    )

    query_service = providers.Factory(CatalogQueryService, session=database_session)

    attribute_validation = providers.Factory(
        AttributeValidationService,
        link_repo=subcategory_attribute_repository,
    )
