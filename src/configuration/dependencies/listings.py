from dependency_injector import containers, providers

from src.core.listings.application.usecases import (
    GetListingCreationSchemaUseCase,
    CreateListingUseCase,
    UpdateListingSchemaUseCase,
    UpdateListingUseCase,
    GetUserListingsUseCase,
    CreateDraftListingUseCase,
    ActivateListingUseCase,
    DeactivateListingUseCase,
    ArchiveListingUseCase,
    DeleteListingUseCase,
    GetPublicListingsUseCase,
    GetDetailPublicListingUseCase,
    SearchListingsUseCase,
)

from src.core.listings.infrastructure.filter_builder import FilterBuilderService
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.listings.infrastructure.listing_unit_of_work import ListingUnitOfWork
from src.core.listings.infrastructure.query_services.listing_query_context import ListingQueryContext
from src.core.references.infrastructure.queries.reference_query_context import ReferenceQueryContext


class ListingContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.listings.routers"
        ]
    )

    session_factory = providers.Dependency()

    listing_unit_of_work = providers.Factory(
        ListingUnitOfWork,
        session_factory=session_factory
    )

    reference_query_context = providers.Factory(
        ReferenceQueryContext,
        session_factory=session_factory
    )

    listing_query_context = providers.Factory(
        ListingQueryContext,
        session_factory=session_factory
    )

    form_builder_service = providers.Factory(ListingFormBuilderService)
    filter_builder_service = providers.Factory(FilterBuilderService)

    listing_creation_schema_usecase = providers.Factory(
        GetListingCreationSchemaUseCase,
        query_service=reference_query_context,
        form_builder=form_builder_service
    )

    create_listing_usecase = providers.Factory(
        CreateListingUseCase,
        unit_of_work=listing_unit_of_work,
        query_service=reference_query_context
    )

    update_listing_schema_usecase = providers.Factory(
        UpdateListingSchemaUseCase,
        listing_query_service=listing_query_context,
        reference_query_service=reference_query_context,
        form_builder=form_builder_service
    )

    update_listing_usecase = providers.Factory(
        UpdateListingUseCase,
        unit_of_work=listing_unit_of_work,
    )

    get_user_listings_usecase = providers.Factory(
        GetUserListingsUseCase,
        query_service=listing_query_context
    )

    create_draft_listing_usecase = providers.Factory(
        CreateDraftListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    activate_listing_usecase = providers.Factory(
        ActivateListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    deactivate_listing_usecase = providers.Factory(
        DeactivateListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    archive_listing_usecase = providers.Factory(
        ArchiveListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    delete_listing_usecase = providers.Factory(
        DeleteListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    get_public_listings_usecase = providers.Factory(
        GetPublicListingsUseCase,
        filter_builder=filter_builder_service,
        query_service=listing_query_context
    )

    get_detail_public_listing_usecase = providers.Factory(
        GetDetailPublicListingUseCase,
        query_service=listing_query_context
    )

    search_listings_usecase = providers.Factory(
        SearchListingsUseCase,
        query_service=listing_query_context
    )
