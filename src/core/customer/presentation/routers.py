from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends, Security
from typing_extensions import Annotated

from src.configuration.dependencies.container import ApplicationContainer
from src.core.customer.application.usecases import ChangeCustomerFullnameUseCase
from src.core.customer.application.usecases.create_customer import CreateCustomerUseCase
from src.core.customer.infrastructure.query import CustomerQueryService
from src.core.customer.presentation.dto import (
    ChangeCustomerFullname,
    CreateCustomerRequest,
    CustomerProfileResponse,
)
from src.core.shared.presentation.dto import CurrentCustomer, CurrentUser
from src.core.shared.presentation.security import get_current_customer, get_current_user

customer_router = APIRouter(prefix="/api/v1/customer", tags=["Customer"])


@customer_router.post("/")
@inject
async def create_customer(
    dto: CreateCustomerRequest,
    usecase: Annotated[
        CreateCustomerUseCase,
        Depends(Provide[ApplicationContainer.customer.create_customer_usecase]),
    ],
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Customer successfully created!"}


@customer_router.patch("/me/change-fullname")
@inject
async def change_customer_fullname(
    dto: ChangeCustomerFullname,
    usecase: Annotated[
        ChangeCustomerFullnameUseCase,
        Depends(
            Provide[ApplicationContainer.customer.change_customer_fullname_usecase]
        ),
    ],
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    await usecase.execute(current_customer.id, dto)
    return {"message": "Ваши данные успешно изменены!"}


@customer_router.get("/me", response_model=CustomerProfileResponse)
@inject
async def get_me(
    service: Annotated[
        CustomerQueryService,
        Depends(Provide[ApplicationContainer.customer.query_service]),
    ],
    current_customer: CurrentCustomer = Security(get_current_customer),
):
    return await service.get_me(current_customer.id)
