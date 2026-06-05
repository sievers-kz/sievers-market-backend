from dependency_injector import containers, providers

from src.core.customer.application.usecases import (
    ChangeCustomerFullnameUseCase,
)
from src.core.customer.application.usecases.create_customer import CreateCustomerUseCase
from src.core.customer.infrastructure.query import CustomerQueryService

from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.infrastructure.repository import CustomerRepository


class CustomerContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()

    query_service = providers.Factory(
        CustomerQueryService,
        session=database_session
    )

    customer_repository = providers.Factory(
        CustomerRepository,
        session=database_session
    )

    uow = providers.Factory(
        CustomerUnitOfWork,
        session=database_session
    )

    change_customer_fullname_usecase = providers.Factory(
        ChangeCustomerFullnameUseCase,
        uow=uow
    )

    create_customer_usecase = providers.Factory(
        CreateCustomerUseCase,
        uow=uow
    )