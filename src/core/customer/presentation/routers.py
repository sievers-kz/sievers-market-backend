from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Security

from src.core.customer.presentation.dependencies import (
    ChangeCustomerFullnameUseCaseDependency,
    CreateCustomerUseCaseDependency,
)
from src.core.customer.presentation.documentation import (
    CHANGE_CUSTOMER_FULLNAME_DOC,
    CREATE_CUSTOMER_DOC,
)
from src.core.customer.presentation.dto import (
    ChangeCustomerFullname,
    CreateCustomerRequest,
)
from src.core.shared.presentation.dto import CurrentCustomer, CurrentUser
from src.core.shared.presentation.security import get_current_customer, get_current_user

customer_router = APIRouter(prefix="/api/v1/customer", tags=["Customer"])


@customer_router.post(
    "/",
    operation_id=CREATE_CUSTOMER_DOC.operation_id,
    summary=CREATE_CUSTOMER_DOC.summary,
    responses=CREATE_CUSTOMER_DOC.responses_doc,
    description=CREATE_CUSTOMER_DOC.description,
)
@inject
async def create_customer(
    dto: CreateCustomerRequest,
    usecase: CreateCustomerUseCaseDependency,
    current_user: CurrentUser = Security(get_current_user),
):
    await usecase.execute(current_user.id, dto)
    return {"message": "Профиль покупателя успешно создан"}


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
