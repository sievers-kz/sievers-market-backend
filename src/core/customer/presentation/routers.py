from uuid import UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, status
from fastapi.params import Security

from src.core.customer.presentation.dependencies import (
    ChangeCustomerFullnameUseCaseDependency,
    CreateOrganizationUseCaseDependency,
    CustomerQueryServiceDependency,
    DeleteOrganizationUseCaseDependency,
)
from src.core.customer.presentation.documentation import (
    CHANGE_CUSTOMER_FULLNAME_DOC,
)
from src.core.customer.presentation.dto import (
    ChangeCustomerFullname,
    CreateOrganizationRequest,
    CreateOrganizationResponse,
    CustomerMeResponse,
    OrganizationListResponse,
    OrganizationResponse,
)
from src.core.shared.presentation.dto import CurrentCustomer
from src.core.shared.presentation.security import get_current_customer

customer_router = APIRouter(prefix="/api/v1/customer", tags=["Customer"])


@customer_router.get("/me", response_model=CustomerMeResponse)
@inject
async def get_me(
    service: CustomerQueryServiceDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_me(current_customer.id)


@customer_router.get("/organization/{organization_id}", response_model=OrganizationResponse)
@inject
async def get_organization(
    organization_id: UUID,
    service: CustomerQueryServiceDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_organization(current_customer.id, organization_id)


@customer_router.get("/organizations", response_model=list[OrganizationListResponse])
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
)
@inject
async def delete_organization(
    organization_id: UUID,
    usecase: DeleteOrganizationUseCaseDependency,
    current_customer: CurrentCustomer = Security(get_current_customer),
) -> None:
    await usecase.execute(current_customer.id, organization_id)
