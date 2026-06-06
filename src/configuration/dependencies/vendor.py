from dependency_injector import containers, providers

from src.core.vendor.application.services.vendor_validation import VendorValidationService
from src.core.vendor.application.usecases import RegisterVendorUseCase, ChangeContactFullnameUseCase, \
    ChangeContactPhoneUseCase, ChangeLogotypeUseCase, ChangeShopNameUseCase
from src.core.vendor.infrastructure.query import VendorQueryService
from src.core.vendor.infrastructure.uow import VendorUnitOfWork
from src.core.vendor.infrastructure.vendor_fetchers import MockVendorFetcher


class VendorContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()
    phone_normalizer = providers.Dependency()

    mock_vendor_fetcher = providers.Factory(MockVendorFetcher)

    uow = providers.Factory(
        VendorUnitOfWork,
        session_factory=session_factory
    )

    create_vendor_usecase = providers.Factory(
        RegisterVendorUseCase,
        uow=uow
    )

    vendor_validation_service = providers.Factory(
        VendorValidationService,
        fetcher=mock_vendor_fetcher
    )

    change_contact_fullname_usecase = providers.Factory(
        ChangeContactFullnameUseCase,
        uow=uow,
    )

    change_contact_phone_usecase = providers.Factory(
        ChangeContactPhoneUseCase,
        uow=uow,
        phone_normalizer=phone_normalizer
    )

    change_logotype_usecase = providers.Factory(
        ChangeLogotypeUseCase,
        uow=uow,
    )

    change_shop_name_usecase = providers.Factory(
        ChangeShopNameUseCase,
        uow=uow,
    )

    query_service = providers.Factory(
        VendorQueryService,
        session=database_session,
    )