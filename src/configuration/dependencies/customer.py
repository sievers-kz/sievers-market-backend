from dependency_injector import containers, providers

from src.core.customer.application.services.customer_service import CustomerService
from src.core.customer.application.services.organization_service import OrganizationService
from src.core.customer.application.services.taxpayer_service import TaxpayerService
from src.core.customer.application.usecases import (
    ChangeCustomerFullnameUseCase,
    CreateOrganizationUseCase,
    DeleteOrganizationUseCase,
    GetOrCreateCustomerUseCase,
)
from src.core.customer.application.usecases.verify_organization_registry import VerifyOrganizationRegistryUseCase
from src.core.customer.infrastructure.gateways.dadata import DaDataTaxpayerGateway
from src.core.customer.infrastructure.gateways.kgd import KGDTaxpayerGateway
from src.core.customer.infrastructure.gateways.mock import MockTaxpayerGateway
from src.core.customer.infrastructure.query_service import CustomerQueryService
from src.core.customer.infrastructure.repository import CustomerRepository
from src.core.customer.infrastructure.uow import CustomerUnitOfWork


class CustomerContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    redis_service = providers.Dependency()
    taxpayer_registry_config = providers.Configuration()
    arq_service = providers.Dependency()

    taxpayer_gateway = providers.Selector(
        taxpayer_registry_config.source,
        dadata=providers.Singleton(
            DaDataTaxpayerGateway,
            api_key=taxpayer_registry_config.dadata_api_key,
        ),
        kgd=providers.Singleton(
            KGDTaxpayerGateway,
            portal_token=taxpayer_registry_config.kgd_portal_token,
        ),
        mock=providers.Singleton(MockTaxpayerGateway),
    )

    customer_repository = providers.Factory(CustomerRepository, session=database_session)

    uow = providers.Factory(CustomerUnitOfWork, session_factory=session_factory)

    query_service = providers.Factory(CustomerQueryService, session=database_session)

    customer_service = providers.Factory(CustomerService, uow=uow)

    organization_service = providers.Factory(OrganizationService, uow=uow)

    change_customer_fullname_usecase = providers.Factory(ChangeCustomerFullnameUseCase, uow=uow)

    taxpayer_service = providers.Factory(TaxpayerService, gateway=taxpayer_gateway)

    verify_organization_registry_usecase = providers.Factory(
        VerifyOrganizationRegistryUseCase, uow=uow, taxpayer_service=taxpayer_service
    )

    create_organization_usecase = providers.Factory(CreateOrganizationUseCase, uow=uow, queue=arq_service)

    get_or_create_customer_usecase = providers.Factory(GetOrCreateCustomerUseCase, uow=uow)

    delete_organization_usecase = providers.Factory(DeleteOrganizationUseCase, uow=uow)
