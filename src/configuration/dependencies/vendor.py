from dependency_injector import containers, providers

from src.core.vendor.application.services.vendor_validation import (
    TaxpayerValidationService,
)
from src.core.vendor.application.usecases import (
    ChangeContactFullnameUseCase,
    ChangeContactPhoneUseCase,
    ChangeLogotypeUseCase,
    ChangeShopNameUseCase,
    RegisterVendorUseCase,
    RestoreVendorUseCase,
)
from src.core.vendor.application.usecases.close_vendor import CloseVendorUseCase
from src.core.vendor.infrastructure.query import VendorCabinetQueryService
from src.core.vendor.infrastructure.repository import VendorRepository
from src.core.vendor.infrastructure.taxpayer_gateway import (
    MockTaxpayerGateway,
    RealTaxpayerGateway,
)
from src.core.vendor.infrastructure.uow import VendorUnitOfWork


class VendorContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    phone_normalizer = providers.Dependency()
    customer_service = providers.Dependency()
    redis_service = providers.Dependency()

    mock_taxpayer_gateway = providers.Factory(MockTaxpayerGateway)
    real_taxpayer_gateway = providers.Factory(RealTaxpayerGateway)

    uow = providers.Factory(VendorUnitOfWork, session_factory=session_factory)

    vendor_repository = providers.Factory(
        VendorRepository,
        session=database_session,
    )

    taxpayer_validation_service = providers.Factory(
        TaxpayerValidationService,
        gateway=mock_taxpayer_gateway,
        cache_service=redis_service,
    )

    register_vendor_usecase = providers.Factory(
        RegisterVendorUseCase,
        uow=uow,
        cache_service=redis_service,
        taxpayer_validation_service=taxpayer_validation_service,
    )

    change_contact_fullname_usecase = providers.Factory(
        ChangeContactFullnameUseCase,
        uow=uow,
    )

    change_contact_phone_usecase = providers.Factory(
        ChangeContactPhoneUseCase, uow=uow, phone_normalizer=phone_normalizer
    )

    change_logotype_usecase = providers.Factory(
        ChangeLogotypeUseCase,
        uow=uow,
    )

    change_shop_name_usecase = providers.Factory(
        ChangeShopNameUseCase,
        uow=uow,
    )

    vendor_cabinet_query_service = providers.Factory(
        VendorCabinetQueryService,
        session=database_session,
    )

    close_vendor_usecase = providers.Factory(
        CloseVendorUseCase,
        uow=uow,
        customer_service=customer_service,
    )

    restore_vendor_usecase = providers.Factory(
        RestoreVendorUseCase,
        uow=uow,
    )
