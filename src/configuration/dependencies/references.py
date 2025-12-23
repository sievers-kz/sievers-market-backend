from dependency_injector import containers, providers

from src.core.references.application.usecases.categories_tree import GetCategoriesTreeUseCase
from src.core.references.infrastructure.queries.reference_query_context import ReferenceQueryContext


class ReferenceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.references.routers"
        ]
    )

    session_factory = providers.Dependency()

    reference_query_context = providers.Factory(
        ReferenceQueryContext,
        session_factory=session_factory
    )

    get_category_tree_usecase = providers.Factory(
        GetCategoriesTreeUseCase,
        query_service=reference_query_context
    )
