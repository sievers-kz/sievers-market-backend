from dependency_injector import containers, providers

from src.core.seller.application.services.seller_service import SellerService

from src.core.seller.application.usecases import (
    BecomeSellerUseCase,
    ChangeFullnameUseCase,
    ChangeCompanyNameUseCase,
    ChangeTaxIDUseCase,
    GetCurrentSellerUseCase
)

from src.core.seller.infrastructure.repository import SellerRepository
from src.core.seller.infrastructure.seller_unit_of_work import SellerUnitOfWork


class SellerContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    session_factory = providers.Dependency()

    seller_repository = providers.Factory(
        SellerRepository,
        session=database_session
    )

    seller_unit_of_work = providers.Factory(
        SellerUnitOfWork,
        session=database_session
    )

    seller_service = providers.Factory(
        SellerService,
        repository=seller_repository
    )

    become_seller_usecase = providers.Factory(
        BecomeSellerUseCase,
        unit_of_work=seller_unit_of_work
    )

    change_fullname_usecase = providers.Factory(
        ChangeFullnameUseCase,
        unit_of_work=seller_unit_of_work
    )

    change_company_name_usecase = providers.Factory(
        ChangeCompanyNameUseCase,
        unit_of_work=seller_unit_of_work
    )

    change_tax_id_usecase = providers.Factory(
        ChangeTaxIDUseCase,
        unit_of_work=seller_unit_of_work
    )

    get_current_seller_usecase = providers.Factory(
        GetCurrentSellerUseCase,
        unit_of_work=seller_unit_of_work
    )
