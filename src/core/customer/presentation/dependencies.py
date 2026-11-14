from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.customer.application.usecases import (
    ChangeCustomerFullnameUseCase,
    ChangeOrganizationContactEmailUseCase,
    ChangeOrganizationContactPhoneUseCase,
    ChangeOrganizationShopNameUseCase,
    CreateOrganizationUseCase,
    DeleteOrganizationUseCase,
)
from src.core.customer.infrastructure.query_service import CustomerQueryService

CustomerQueryServiceDependency = Annotated[
    CustomerQueryService, Depends(Provide[ApplicationContainer.customer.query_service])
]

ChangeCustomerFullnameUseCaseDependency = Annotated[
    ChangeCustomerFullnameUseCase,
    Depends(Provide[ApplicationContainer.customer.change_customer_fullname_usecase]),
]

CreateOrganizationUseCaseDependency = Annotated[
    CreateOrganizationUseCase,
    Depends(Provide[ApplicationContainer.customer.create_organization_usecase]),
]

DeleteOrganizationUseCaseDependency = Annotated[
    DeleteOrganizationUseCase,
    Depends(Provide[ApplicationContainer.customer.delete_organization_usecase]),
]

ChangeOrganizationShopNameUseCaseDependency = Annotated[
    ChangeOrganizationShopNameUseCase,
    Depends(Provide[ApplicationContainer.customer.change_organization_shop_name_usecase]),
]

ChangeOrganizationContactPhoneUseCaseDependency = Annotated[
    ChangeOrganizationContactPhoneUseCase,
    Depends(Provide[ApplicationContainer.customer.change_organization_contact_phone_usecase]),
]

ChangeOrganizationContactEmailUseCaseDependency = Annotated[
    ChangeOrganizationContactEmailUseCase,
    Depends(Provide[ApplicationContainer.customer.change_organization_contact_email_usecase]),
]
