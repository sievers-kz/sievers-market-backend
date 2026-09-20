from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Query, Security

from src.core.listing.presentation.dependencies import (
    ActivateListingUseCaseDependency,
    ArchiveListingUseCaseDependency,
    ChangeListingAttributeUseCaseDependency,
    ChangeListingDescriptionUseCaseDependency,
    ChangeListingLocationUseCaseDependency,
    ChangeListingPriceUseCaseDependency,
    CreateListingUseCaseDependency,
    DeactivateListingUseCaseDependency,
    DeleteListingUseCaseDependency,
    ListingQueryServiceDependency,
    ListingSearchServiceDependency,
)
from src.core.listing.presentation.documentation import (
    ACTIVATE_LISTING_DOC,
    ARCHIVE_LISTING_DOC,
    CHANGE_LISTING_ATTRIBUTE_DOC,
    CHANGE_LISTING_DESCRIPTION_DOC,
    CHANGE_LISTING_LOCATION_DOC,
    CHANGE_LISTING_PRICE_DOC,
    CREATE_LISTING_DOC,
    DEACTIVATE_LISTING_DOC,
    DELETE_LISTING_DOC,
    GET_LISTING_DETAILS_DOC,
    GET_LISTINGS_CATALOG_DOC,
    SEARCH_LISTING_DOC,
)
from src.core.listing.presentation.dto import (
    ChangeListingAttributeRequest,
    ChangeListingDescriptionRequest,
    ChangeListingLocationRequest,
    ChangeListingPriceRequest,
    CreateListingRequest,
    ListingCardResponse,
    ListingDetailResponse,
    ListingSearchQuery,
)
from src.core.shared.presentation.dto import CurrentVendor, PaginatedResponse
from src.core.shared.presentation.security import get_current_vendor

listing_router = APIRouter(prefix="/api/v1/listing", tags=["Listing"])


@listing_router.post(
    "/",
    operation_id=CREATE_LISTING_DOC.operation_id,
    summary=CREATE_LISTING_DOC.summary,
    responses=CREATE_LISTING_DOC.responses_doc,
    description=CREATE_LISTING_DOC.description,
)
@inject
async def create_listing(
    dto: CreateListingRequest,
    usecase: CreateListingUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    respone = await usecase.execute(current_vendor.id, dto)
    return {"message": "Объявление создано", "response": respone}


@listing_router.patch(
    "/{listing_id}/price",
    operation_id=CHANGE_LISTING_PRICE_DOC.operation_id,
    summary=CHANGE_LISTING_PRICE_DOC.summary,
    responses=CHANGE_LISTING_PRICE_DOC.responses_doc,
    description=CHANGE_LISTING_PRICE_DOC.description,
)
@inject
async def change_listing_price(
    listing_id: UUID,
    dto: ChangeListingPriceRequest,
    usecase: ChangeListingPriceUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id, dto)
    return {"message": "Цена объявления обновлена"}


@listing_router.patch(
    "/{listing_id}/location",
    operation_id=CHANGE_LISTING_LOCATION_DOC.operation_id,
    summary=CHANGE_LISTING_LOCATION_DOC.summary,
    responses=CHANGE_LISTING_LOCATION_DOC.responses_doc,
    description=CHANGE_LISTING_LOCATION_DOC.description,
)
@inject
async def change_listing_location(
    listing_id: UUID,
    dto: ChangeListingLocationRequest,
    usecase: ChangeListingLocationUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id, dto)
    return {"message": "Местоположение объявления изменены"}


@listing_router.patch(
    "/{listing_id}/description",
    operation_id=CHANGE_LISTING_DESCRIPTION_DOC.operation_id,
    summary=CHANGE_LISTING_DESCRIPTION_DOC.summary,
    responses=CHANGE_LISTING_DESCRIPTION_DOC.responses_doc,
    description=CHANGE_LISTING_DESCRIPTION_DOC.description,
)
@inject
async def change_listing_description(
    listing_id: UUID,
    dto: ChangeListingDescriptionRequest,
    usecase: ChangeListingDescriptionUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id, dto)
    return {"message": "Описание объявления изменено"}


@listing_router.patch(
    "/{listing_id}/attributes",
    operation_id=CHANGE_LISTING_ATTRIBUTE_DOC.operation_id,
    summary=CHANGE_LISTING_ATTRIBUTE_DOC.summary,
    responses=CHANGE_LISTING_ATTRIBUTE_DOC.responses_doc,
    description=CHANGE_LISTING_ATTRIBUTE_DOC.description,
)
@inject
async def change_listing_attribute(
    listing_id: UUID,
    dto: ChangeListingAttributeRequest,
    usecase: ChangeListingAttributeUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id, dto)
    return {"message": "Атрибуты объявления обновлены"}


@listing_router.patch(
    "/{listing_id}/activate",
    operation_id=ACTIVATE_LISTING_DOC.operation_id,
    summary=ACTIVATE_LISTING_DOC.summary,
    responses=ACTIVATE_LISTING_DOC.responses_doc,
    description=ACTIVATE_LISTING_DOC.description,
)
@inject
async def activate_listing(
    listing_id: UUID,
    usecase: ActivateListingUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление активировано"}


@listing_router.patch(
    "/{listing_id}/deactivate",
    operation_id=DEACTIVATE_LISTING_DOC.operation_id,
    summary=DEACTIVATE_LISTING_DOC.summary,
    responses=DEACTIVATE_LISTING_DOC.responses_doc,
    description=DEACTIVATE_LISTING_DOC.description,
)
@inject
async def deactivate_listing(
    listing_id: UUID,
    usecase: DeactivateListingUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление деактивировано"}


@listing_router.patch(
    "/{listing_id}/archive",
    operation_id=ARCHIVE_LISTING_DOC.operation_id,
    summary=ARCHIVE_LISTING_DOC.summary,
    responses=ARCHIVE_LISTING_DOC.responses_doc,
    description=ARCHIVE_LISTING_DOC.description,
)
@inject
async def archive_listing(
    listing_id: UUID,
    usecase: ArchiveListingUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление архивировано"}


@listing_router.patch(
    "/{listing_id}/delete",
    operation_id=DELETE_LISTING_DOC.operation_id,
    summary=DELETE_LISTING_DOC.summary,
    responses=DELETE_LISTING_DOC.responses_doc,
    description=DELETE_LISTING_DOC.description,
)
@inject
async def delete_listing(
    listing_id: UUID,
    usecase: DeleteListingUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, listing_id)
    return {"message": "Объявление удалено"}


@listing_router.post(
    "/search",
    operation_id=SEARCH_LISTING_DOC.operation_id,
    summary=SEARCH_LISTING_DOC.summary,
    responses=SEARCH_LISTING_DOC.responses_doc,
    description=SEARCH_LISTING_DOC.description,
)
@inject
async def search_listing(
    params: ListingSearchQuery,
    service: ListingSearchServiceDependency,
):
    return await service.search_listings(params)


@listing_router.get(
    "/catalog",
    response_model=PaginatedResponse[ListingCardResponse],
    operation_id=GET_LISTINGS_CATALOG_DOC.operation_id,
    summary=GET_LISTINGS_CATALOG_DOC.summary,
    responses=GET_LISTINGS_CATALOG_DOC.responses_doc,
    description=GET_LISTINGS_CATALOG_DOC.description,
)
@inject
async def get_listings_catalog(
    service: ListingQueryServiceDependency,
    category_id: UUID = Query(alias="category_id"),
    subcategory_id: UUID | None = Query(None, alias="subcategory_id"),
    page: int = Query(1, alias="page"),
    limit: int = Query(20, alias="limit"),
):
    return await service.get_listings_card(category_id, subcategory_id, page, limit)


@listing_router.get(
    "/{listing_id}",
    response_model=ListingDetailResponse | None,
    operation_id=GET_LISTING_DETAILS_DOC.operation_id,
    summary=GET_LISTING_DETAILS_DOC.summary,
    responses=GET_LISTING_DETAILS_DOC.responses_doc,
    description=GET_LISTING_DETAILS_DOC.description,
)
@inject
async def get_listing_details(
    listing_id: UUID,
    service: ListingQueryServiceDependency,
):
    return await service.get_listing_details(listing_id)
