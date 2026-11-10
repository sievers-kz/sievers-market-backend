from dependency_injector import containers, providers

from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.application.usecases import (
    ActivateListingUseCase,
    ArchiveListingUseCase,
    ChangeListingAttributeUseCase,
    ChangeListingDescriptionUseCase,
    ChangeListingLocationUseCase,
    ChangeListingPriceUseCase,
    CreateListingUseCase,
    DeactivateListingUseCase,
    DeleteListingUseCase,
)
from src.core.listing.infrastructure.query import ListingQueryService
from src.core.listing.infrastructure.repository import ListingRepository
from src.core.listing.infrastructure.uow import ListingUnitOfWork


class ListingContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    attribute_validation = providers.Dependency()
    meilisearch_service = providers.Dependency()
    organization_service = providers.Dependency()

    uow = providers.Factory(ListingUnitOfWork, session_factory=session_factory)

    listing_search_service = providers.Factory(
        ListingSearchService,
        search_service=meilisearch_service,
    )

    listing_repository = providers.Factory(
        ListingRepository,
        session=database_session,
    )

    create_listing_usecase = providers.Factory(
        CreateListingUseCase,
        uow=uow,
        attribute_validation=attribute_validation,
        listing_search_service=listing_search_service,
        organization_service=organization_service,
    )

    change_listing_price_usecase = providers.Factory(
        ChangeListingPriceUseCase,
        uow=uow,
        listing_search_service=listing_search_service,
        organization_service=organization_service,
    )

    change_listing_location_usecase = providers.Factory(
        ChangeListingLocationUseCase,
        uow=uow,
        listing_search_service=listing_search_service,
        organization_service=organization_service,
    )

    change_listing_description_usecase = providers.Factory(
        ChangeListingDescriptionUseCase,
        uow=uow,
        organization_service=organization_service,
    )

    change_listing_attribute_usecase = providers.Factory(
        ChangeListingAttributeUseCase,
        uow=uow,
        attribute_validation=attribute_validation,
        organization_service=organization_service,
    )

    activate_listing_usecase = providers.Factory(
        ActivateListingUseCase,
        uow=uow,
        organization_service=organization_service,
    )

    deactivate_listing_usecase = providers.Factory(
        DeactivateListingUseCase,
        uow=uow,
        organization_service=organization_service,
    )

    archive_listing_usecase = providers.Factory(
        ArchiveListingUseCase,
        uow=uow,
        organization_service=organization_service,
    )

    delete_listing_usecase = providers.Factory(
        DeleteListingUseCase,
        uow=uow,
        organization_service=organization_service,
    )

    query_service = providers.Factory(
        ListingQueryService,
        session=database_session,
    )
