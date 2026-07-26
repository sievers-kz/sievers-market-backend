from dependency_injector import containers, providers

from src.core.customer.application.services.customer_service import CustomerService
from src.core.customer.application.usecases import ChangeCustomerFullnameUseCase
from src.core.customer.application.usecases.create_customer import CreateCustomerUseCase
from src.core.customer.infrastructure.query import CustomerQueryService
from src.core.customer.infrastructure.repository import CustomerRepository
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class CustomerContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    query_service = providers.Factory(CustomerQueryService, session=database_session)

    customer_repository = providers.Factory(
        CustomerRepository, session=database_session
    )

    uow = providers.Factory(CustomerUnitOfWork, session_factory=session_factory)

    customer_service = providers.Factory(CustomerService, uow=uow)

    change_customer_fullname_usecase = providers.Factory(
        ChangeCustomerFullnameUseCase, uow=uow
    )

    create_customer_usecase = providers.Factory(CreateCustomerUseCase, uow=uow)
