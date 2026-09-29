from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.customer.application.usecases import ChangeCustomerFullnameUseCase
from src.core.customer.application.usecases.create_customer import CreateCustomerUseCase

CreateCustomerUseCaseDependency = Annotated[
    CreateCustomerUseCase,
    Depends(Provide[ApplicationContainer.customer.create_customer_usecase]),
]

ChangeCustomerFullnameUseCaseDependency = Annotated[
    ChangeCustomerFullnameUseCase,
    Depends(Provide[ApplicationContainer.customer.change_customer_fullname_usecase]),
]
