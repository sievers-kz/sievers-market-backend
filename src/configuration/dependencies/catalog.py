from dependency_injector import containers, providers

from src.core.catalog.application.services.category import CategoryService
from src.core.catalog.application.services.rubric import RubricService
from src.core.catalog.application.services.subcategory import SubcategoryService
from src.core.catalog.infrastructure.query import CatalogQueryService
from src.core.catalog.infrastructure.uow import CatalogUnitOfWork


class CatalogContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    catalog_unit_of_work = providers.Factory(
        CatalogUnitOfWork,
        session_factory=session_factory
    )

    rubric_service = providers.Factory(
        RubricService,
        uow=catalog_unit_of_work
    )

    category_service = providers.Factory(
        CategoryService,
        uow=catalog_unit_of_work
    )

    subcategory_service = providers.Factory(
        SubcategoryService,
        uow=catalog_unit_of_work
    )

    query_service = providers.Factory(
        CatalogQueryService,
        session=database_session
    )
