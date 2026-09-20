from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.vendor.application.services.vendor_validation import (
    TaxpayerValidationService,
)
from src.core.vendor.application.usecases import (
    ChangeContactFullnameUseCase,
    ChangeContactPhoneUseCase,
    ChangeLogotypeUseCase,
    ChangeShopNameUseCase,
    CloseVendorUseCase,
    RegisterVendorUseCase,
    RestoreVendorUseCase,
)
from src.core.vendor.infrastructure.query import VendorQueryService

TaxpayerValidationServiceDependency = Annotated[
    TaxpayerValidationService,
    Depends(Provide[ApplicationContainer.vendor.taxpayer_validation_service]),
]

RegisterVendorUseCaseDependency = Annotated[
    RegisterVendorUseCase,
    Depends(Provide[ApplicationContainer.vendor.register_vendor_usecase]),
]

ChangeContactFullnameUseCaseDependency = Annotated[
    ChangeContactFullnameUseCase,
    Depends(Provide[ApplicationContainer.vendor.change_contact_fullname_usecase]),
]

ChangeContactPhoneUseCaseDependency = Annotated[
    ChangeContactPhoneUseCase,
    Depends(Provide[ApplicationContainer.vendor.change_contact_phone_usecase]),
]

ChangeShopNameUseCaseDependency = Annotated[
    ChangeShopNameUseCase,
    Depends(Provide[ApplicationContainer.vendor.change_shop_name_usecase]),
]

ChangeLogotypeUseCaseDependency = Annotated[
    ChangeLogotypeUseCase,
    Depends(Provide[ApplicationContainer.vendor.change_logotype_usecase]),
]

VendorQueryServiceDependency = Annotated[
    VendorQueryService,
    Depends(Provide[ApplicationContainer.vendor.query_service]),
]

CloseVendorUseCaseDependency = Annotated[
    CloseVendorUseCase,
    Depends(Provide[ApplicationContainer.vendor.close_vendor_usecase]),
]

RestoreVendorUseCaseDependency = Annotated[
    RestoreVendorUseCase,
    Depends(Provide[ApplicationContainer.vendor.restore_vendor_usecase]),
]
