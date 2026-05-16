from dependency_injector import containers, providers

from src.core.listing.application.usecases import CreateListingUseCase, ChangeListingAttributeUseCase, \
    ChangeListingPriceUseCase, ChangeListingLocationUseCase, ChangeListingDescriptionUseCase
from src.core.listing.infrastructure.uow import ListingUnitOfWork


class ListingContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    customer_repository = providers.Dependency()
    subcategory_service = providers.Dependency()

    uow = providers.Factory(
        ListingUnitOfWork,
        session=database_session,
    )

    create_listing_usecase = providers.Factory(
        CreateListingUseCase,
        uow=uow,
        subcategory_service=subcategory_service,
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
        subcategory_service=subcategory_service,
    )
