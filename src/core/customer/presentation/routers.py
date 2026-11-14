from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, status
from fastapi.params import Security

from src.core.customer.presentation.dependencies import (
    ChangeCustomerFullnameUseCaseDependency,
    ChangeOrganizationContactEmailUseCaseDependency,
    ChangeOrganizationContactPhoneUseCaseDependency,
    ChangeOrganizationShopNameUseCaseDependency,
    CreateOrganizationUseCaseDependency,
    CustomerQueryServiceDependency,
    DeleteOrganizationUseCaseDependency,
)
from src.core.customer.presentation.documentation import (
    CHANGE_CUSTOMER_FULLNAME_DOC,
    CHANGE_ORGANIZATION_CONTACT_EMAIL_DOC,
    CHANGE_ORGANIZATION_CONTACT_PHONE_DOC,
    CHANGE_ORGANIZATION_SHOP_NAME_DOC,
    CREATE_ORGANIZATION_DOC,
    DELETE_ORGANIZATION_DOC,
    GET_CUSTOMER_ME_DOC,
    GET_ORGANIZATION_DOC,
    GET_ORGANIZATIONS_DOC,
)
from src.core.customer.presentation.dto import (
    ChangeCustomerFullname,
    ChangeOrganizationContactEmailRequest,
    ChangeOrganizationContactPhoneRequest,
    ChangeOrganizationShopNameRequest,
    CreateOrganizationRequest,
    CreateOrganizationResponse,
    CustomerMeResponse,
    OrganizationListResponse,
    OrganizationResponse,
)
from src.core.shared.presentation.dto import CurrentCustomer
from src.core.shared.presentation.security import get_current_customer

customer_router = APIRouter(prefix="/api/v1/customer", tags=["Customer"])


@customer_router.get(
    "/me",
    response_model=CustomerMeResponse,
    operation_id=GET_CUSTOMER_ME_DOC.operation_id,
    summary=GET_CUSTOMER_ME_DOC.summary,
    responses=GET_CUSTOMER_ME_DOC.responses_doc,
    description=GET_CUSTOMER_ME_DOC.description,
)
@inject
async def get_me(
    service: CustomerQueryServiceDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_me(current_customer.id)


@customer_router.get(
    "/organization/{organization_id}",
    response_model=OrganizationResponse,
    operation_id=GET_ORGANIZATION_DOC.operation_id,
    summary=GET_ORGANIZATION_DOC.summary,
    responses=GET_ORGANIZATION_DOC.responses_doc,
    description=GET_ORGANIZATION_DOC.description,
)
@inject
async def get_organization(
    organization_id: UUID,
    service: CustomerQueryServiceDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_organization(current_customer.id, organization_id)


@customer_router.get(
    "/organizations",
    response_model=list[OrganizationListResponse],
    operation_id=GET_ORGANIZATIONS_DOC.operation_id,
    summary=GET_ORGANIZATIONS_DOC.summary,
    responses=GET_ORGANIZATIONS_DOC.responses_doc,
    description=GET_ORGANIZATIONS_DOC.description,
)
@inject
async def get_organizations(
    service: CustomerQueryServiceDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_organizations(current_customer.id)


@customer_router.patch(
    "/fullname/change",
    operation_id=CHANGE_CUSTOMER_FULLNAME_DOC.operation_id,
    summary=CHANGE_CUSTOMER_FULLNAME_DOC.summary,
    responses=CHANGE_CUSTOMER_FULLNAME_DOC.responses_doc,
    description=CHANGE_CUSTOMER_FULLNAME_DOC.description,
)
@inject
async def change_customer_fullname(
    dto: ChangeCustomerFullname,
    usecase: ChangeCustomerFullnameUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    await usecase.execute(current_customer.id, dto)
    return {"message": "ФИО успешно изменены"}


@customer_router.post(
    "/organization",
    response_model=CreateOrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id=CREATE_ORGANIZATION_DOC.operation_id,
    summary=CREATE_ORGANIZATION_DOC.summary,
    responses=CREATE_ORGANIZATION_DOC.responses_doc,
    description=CREATE_ORGANIZATION_DOC.description,
)
@inject
async def create_organization(
    dto: CreateOrganizationRequest,
    usecase: CreateOrganizationUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await usecase.execute(current_customer.id, dto)


@customer_router.delete(
    "/organization/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id=DELETE_ORGANIZATION_DOC.operation_id,
    summary=DELETE_ORGANIZATION_DOC.summary,
    responses=DELETE_ORGANIZATION_DOC.responses_doc,
    description=DELETE_ORGANIZATION_DOC.description,
)
@inject
async def delete_organization(
    organization_id: UUID,
    usecase: DeleteOrganizationUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
) -> None:
    await usecase.execute(current_customer.id, organization_id)


@customer_router.patch(
    "/organization/{organization_id}/shop-name",
    operation_id=CHANGE_ORGANIZATION_SHOP_NAME_DOC.operation_id,
    summary=CHANGE_ORGANIZATION_SHOP_NAME_DOC.summary,
    responses=CHANGE_ORGANIZATION_SHOP_NAME_DOC.responses_doc,
    description=CHANGE_ORGANIZATION_SHOP_NAME_DOC.description,
)
@inject
async def change_organization_shop_name(
    organization_id: UUID,
    dto: ChangeOrganizationShopNameRequest,
    usecase: ChangeOrganizationShopNameUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    await usecase.execute(current_customer.id, organization_id, dto)
    return {"message": "Название магазина успешно изменено"}


@customer_router.patch(
    "/organization/{organization_id}/contact-phone",
    operation_id=CHANGE_ORGANIZATION_CONTACT_PHONE_DOC.operation_id,
    summary=CHANGE_ORGANIZATION_CONTACT_PHONE_DOC.summary,
    responses=CHANGE_ORGANIZATION_CONTACT_PHONE_DOC.responses_doc,
    description=CHANGE_ORGANIZATION_CONTACT_PHONE_DOC.description,
)
@inject
async def change_organization_contact_phone(
    organization_id: UUID,
    dto: ChangeOrganizationContactPhoneRequest,
    usecase: ChangeOrganizationContactPhoneUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    await usecase.execute(current_customer.id, organization_id, dto)
    return {"message": "Контактный телефон успешно изменён"}


@customer_router.patch(
    "/organization/{organization_id}/contact-email",
    operation_id=CHANGE_ORGANIZATION_CONTACT_EMAIL_DOC.operation_id,
    summary=CHANGE_ORGANIZATION_CONTACT_EMAIL_DOC.summary,
    responses=CHANGE_ORGANIZATION_CONTACT_EMAIL_DOC.responses_doc,
    description=CHANGE_ORGANIZATION_CONTACT_EMAIL_DOC.description,
)
@inject
async def change_organization_contact_email(
    organization_id: UUID,
    dto: ChangeOrganizationContactEmailRequest,
    usecase: ChangeOrganizationContactEmailUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    await usecase.execute(current_customer.id, organization_id, dto)
    return {"message": "Контактный email успешно изменён"}
