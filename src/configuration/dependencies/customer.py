from dependency_injector import containers, providers

from src.core.customer.application.services.customer_service import CustomerService
from src.core.customer.application.usecases import (
    ChangeCustomerRegionUseCase,
    ChangeCustomerFullnameUseCase,
    GetCurrentCustomerUseCase
)

from src.core.customer.infrastructure.adapters.region_checker import RegionCheckerAdapter
from src.core.customer.infrastructure.uow import CustomerUnitOfWork
from src.core.customer.infrastructure.repository import CustomerRepository


class CustomerContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    session_factory = providers.Dependency()
    region_service = providers.Dependency()

    customer_repository = providers.Factory(
        CustomerRepository,
        session=database_session
    )

    customer_unit_of_work = providers.Factory(
        CustomerUnitOfWork,
        session=database_session
    )

    customer_service = providers.Factory(
        CustomerService,
        repository=customer_repository
    )

    region_checker_adapter = providers.Factory(
        RegionCheckerAdapter,
        region_service=region_service
    )

    change_customer_region_usecase = providers.Factory(
        ChangeCustomerRegionUseCase,
        unit_of_work=customer_unit_of_work,
        region_checker=region_checker_adapter
    )

    change_customer_fullname_usecase = providers.Factory(
        ChangeCustomerFullnameUseCase,
        unit_of_work=customer_unit_of_work
    )

    get_current_customer_usecase = providers.Factory(
        GetCurrentCustomerUseCase,
        unit_of_work=customer_unit_of_work
    )
