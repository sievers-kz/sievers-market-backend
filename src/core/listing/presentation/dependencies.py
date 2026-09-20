from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
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

CreateListingUseCaseDependency = Annotated[
    CreateListingUseCase,
    Depends(Provide[ApplicationContainer.listing.create_listing_usecase]),
]

ChangeListingPriceUseCaseDependency = Annotated[
    ChangeListingPriceUseCase,
    Depends(Provide[ApplicationContainer.listing.change_listing_price_usecase]),
]

ChangeListingLocationUseCaseDependency = Annotated[
    ChangeListingLocationUseCase,
    Depends(Provide[ApplicationContainer.listing.change_listing_location_usecase]),
]

ChangeListingDescriptionUseCaseDependency = Annotated[
    ChangeListingDescriptionUseCase,
    Depends(Provide[ApplicationContainer.listing.change_listing_description_usecase]),
]

ChangeListingAttributeUseCaseDependency = Annotated[
    ChangeListingAttributeUseCase,
    Depends(Provide[ApplicationContainer.listing.change_listing_attribute_usecase]),
]

ActivateListingUseCaseDependency = Annotated[
    ActivateListingUseCase,
    Depends(Provide[ApplicationContainer.listing.activate_listing_usecase]),
]

DeactivateListingUseCaseDependency = Annotated[
    DeactivateListingUseCase,
    Depends(Provide[ApplicationContainer.listing.deactivate_listing_usecase]),
]

ArchiveListingUseCaseDependency = Annotated[
    ArchiveListingUseCase,
    Depends(Provide[ApplicationContainer.listing.archive_listing_usecase]),
]

DeleteListingUseCaseDependency = Annotated[
    DeleteListingUseCase,
    Depends(Provide[ApplicationContainer.listing.delete_listing_usecase]),
]

ListingSearchServiceDependency = Annotated[
    ListingSearchService,
    Depends(Provide[ApplicationContainer.listing.listing_search_service]),
]

ListingQueryServiceDependency = Annotated[
    ListingQueryService,
    Depends(Provide[ApplicationContainer.listing.query_service]),
]
