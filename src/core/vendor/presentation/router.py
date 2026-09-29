from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Query, Security

from src.core.listing.domain.enums import ListingStatus
from src.core.shared.presentation.dto import (
    CurrentUser,
    CurrentVendor,
    PaginatedResponse,
)
from src.core.shared.presentation.security import get_current_user, get_current_vendor
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.presentation.dependencies import (
    ChangeContactFullnameUseCaseDependency,
    ChangeContactPhoneUseCaseDependency,
    ChangeLogotypeUseCaseDependency,
    ChangeShopNameUseCaseDependency,
    CloseVendorUseCaseDependency,
    RegisterVendorUseCaseDependency,
    RestoreVendorUseCaseDependency,
    TaxpayerValidationServiceDependency,
    VendorQueryServiceDependency,
)
from src.core.vendor.presentation.documentation import (
    CHANGE_CONTACT_FULLNAME_DOC,
    CHANGE_CONTACT_PHONE_DOC,
    CHANGE_LOGOTYPE_DOC,
    CHANGE_SHOP_NAME_DOC,
    CLOSE_VENDOR_DOC,
    CREATE_VENDOR_DOC,
    GET_ME_LISTINGS_DOC,
    GET_VENDOR_CATALOG_DOC,
    GET_VENDOR_DETAILS_DOC,
    RESTORE_VENDOR_DOC,
    VERIFY_TAXPAYER_DOC,
)
from src.core.vendor.presentation.dto import (
    ChangeContactFullnameRequest,
    ChangeContactPhoneRequest,
    ChangeLogotypeRequest,
    ChangeShopNameRequest,
    CreateVendorRequest,
    DetailVendorResponse,
    TaxpayerResponse,
    VendorCardResponse,
    VendorListingCardsResponse,
)

vendor_router = APIRouter(prefix="/api/v1/vendor", tags=["Vendor"])


@vendor_router.get(
    "/taxpayer/{tax_id}",
    response_model=TaxpayerResponse,
    operation_id=VERIFY_TAXPAYER_DOC.operation_id,
    summary=VERIFY_TAXPAYER_DOC.summary,
    responses=VERIFY_TAXPAYER_DOC.responses_doc,
    description=VERIFY_TAXPAYER_DOC.description,
)
@inject
async def verify_taxpayer(
    tax_id: str,
    service: TaxpayerValidationServiceDependency,
    legal_form: LegalForm = Query(..., alias="legal_form"),
    current_user: CurrentUser = Security(get_current_user),
):
    return await service.validate(tax_id, legal_form)


@vendor_router.post(
    "/",
    operation_id=CREATE_VENDOR_DOC.operation_id,
    summary=CREATE_VENDOR_DOC.summary,
    responses=CREATE_VENDOR_DOC.responses_doc,
    description=CREATE_VENDOR_DOC.description,
)
@inject
async def create_vendor(
    dto: CreateVendorRequest,
    usecase: RegisterVendorUseCaseDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Профиль продавца успешно создан"}


@vendor_router.patch(
    "/contact-fullname",
    operation_id=CHANGE_CONTACT_FULLNAME_DOC.operation_id,
    summary=CHANGE_CONTACT_FULLNAME_DOC.summary,
    responses=CHANGE_CONTACT_FULLNAME_DOC.responses_doc,
    description=CHANGE_CONTACT_FULLNAME_DOC.description,
)
@inject
async def change_contact_fullname(
    dto: ChangeContactFullnameRequest,
    usecase: ChangeContactFullnameUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Контактное ФИО обновлено"}


@vendor_router.patch(
    "/contact-phone",
    operation_id=CHANGE_CONTACT_PHONE_DOC.operation_id,
    summary=CHANGE_CONTACT_PHONE_DOC.summary,
    responses=CHANGE_CONTACT_PHONE_DOC.responses_doc,
    description=CHANGE_CONTACT_PHONE_DOC.description,
)
@inject
async def change_contact_phone(
    dto: ChangeContactPhoneRequest,
    usecase: ChangeContactPhoneUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Контактный номер телефона обновлен"}


@vendor_router.patch(
    "/shop-name",
    operation_id=CHANGE_SHOP_NAME_DOC.operation_id,
    summary=CHANGE_SHOP_NAME_DOC.summary,
    responses=CHANGE_SHOP_NAME_DOC.responses_doc,
    description=CHANGE_SHOP_NAME_DOC.description,
)
@inject
async def change_shop_name(
    dto: ChangeShopNameRequest,
    usecase: ChangeShopNameUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Имя магазина успешно изменено"}


@vendor_router.patch(
    "/logotype/change",
    operation_id=CHANGE_LOGOTYPE_DOC.operation_id,
    summary=CHANGE_LOGOTYPE_DOC.summary,
    responses=CHANGE_LOGOTYPE_DOC.responses_doc,
    description=CHANGE_LOGOTYPE_DOC.description,
)
@inject
async def change_logotype(
    dto: ChangeLogotypeRequest,
    usecase: ChangeLogotypeUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id, dto)
    return {"message": "Логотип успешно обновлен"}


@vendor_router.get(
    "/me/listings/{status}",
    response_model=PaginatedResponse[VendorListingCardsResponse],
    operation_id=GET_ME_LISTINGS_DOC.operation_id,
    summary=GET_ME_LISTINGS_DOC.summary,
    responses=GET_ME_LISTINGS_DOC.responses_doc,
    description=GET_ME_LISTINGS_DOC.description,
)
@inject
async def get_me_listings(
    status: ListingStatus,
    service: VendorQueryServiceDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
    page: int = Query(1, alias="page"),
    limit: int = Query(10, alias="limit"),
):
    return await service.get_vendor_listing_cards_by_status(current_vendor.id, status, page, limit)


@vendor_router.patch(
    "/close",
    operation_id=CLOSE_VENDOR_DOC.operation_id,
    summary=CLOSE_VENDOR_DOC.summary,
    responses=CLOSE_VENDOR_DOC.responses_doc,
    description=CLOSE_VENDOR_DOC.description,
)
@inject
async def close_vendor(
    usecase: CloseVendorUseCaseDependency,
    current_vendor: CurrentVendor = Security(get_current_vendor),
):
    await usecase.execute(current_vendor.id)
    return {"message": "Аккаунт продавца закрыт"}


@vendor_router.patch(
    "/restore",
    operation_id=RESTORE_VENDOR_DOC.operation_id,
    summary=RESTORE_VENDOR_DOC.summary,
    responses=RESTORE_VENDOR_DOC.responses_doc,
    description=RESTORE_VENDOR_DOC.description,
)
@inject
async def restore_vendor(
    usecase: RestoreVendorUseCaseDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id)
    return {"message": "Профиль продавца восстановлен"}


@vendor_router.get(
    "/catalog",
    response_model=PaginatedResponse[VendorCardResponse],
    operation_id=GET_VENDOR_CATALOG_DOC.operation_id,
    summary=GET_VENDOR_CATALOG_DOC.summary,
    responses=GET_VENDOR_CATALOG_DOC.responses_doc,
    description=GET_VENDOR_CATALOG_DOC.description,
)
@inject
async def get_vendor_catalog(
    service: VendorQueryServiceDependency,
    page: int = Query(1, alias="page"),
    limit: int = Query(20, alias="limit"),
):
    return await service.get_vendors_card(page, limit)


@vendor_router.get(
    "/{vendor_id}",
    response_model=DetailVendorResponse,
    operation_id=GET_VENDOR_DETAILS_DOC.operation_id,
    summary=GET_VENDOR_DETAILS_DOC.summary,
    responses=GET_VENDOR_DETAILS_DOC.responses_doc,
    description=GET_VENDOR_DETAILS_DOC.description,
)
@inject
async def get_vendor_details(
    vendor_id: UUID,
    service: VendorQueryServiceDependency,
):
    return await service.get_vendor_details(vendor_id)
