from dependency_injector import containers, providers

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
from src.core.listing.infrastructure.repository import ListingRepository
from src.core.listing.infrastructure.uow import ListingUnitOfWork


class ListingContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    attribute_validation = providers.Dependency()

    uow = providers.Factory(ListingUnitOfWork, session_factory=session_factory)

    listing_repository = providers.Factory(
        ListingRepository,
        session=database_session,
    )

    create_listing_usecase = providers.Factory(
        CreateListingUseCase,
        uow=uow,
        attribute_validation=attribute_validation,
    )

    change_listing_price_usecase = providers.Factory(
        ChangeListingPriceUseCase,
        uow=uow,
    )

    change_listing_location_usecase = providers.Factory(
        ChangeListingLocationUseCase,
        uow=uow,
    )

    change_listing_description_usecase = providers.Factory(
        ChangeListingDescriptionUseCase,
        uow=uow,
    )

    change_listing_attribute_usecase = providers.Factory(
        ChangeListingAttributeUseCase,
        uow=uow,
        attribute_validation=attribute_validation,
    )

    activate_listing_usecase = providers.Factory(
        ActivateListingUseCase,
        uow=uow,
    )

    deactivate_listing_usecase = providers.Factory(
        DeactivateListingUseCase,
        uow=uow,
    )

    archive_listing_usecase = providers.Factory(
        ArchiveListingUseCase,
        uow=uow,
    )

    delete_listing_usecase = providers.Factory(
        DeleteListingUseCase,
        uow=uow,
    )
