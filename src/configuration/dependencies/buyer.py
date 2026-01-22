from dependency_injector import containers, providers

from src.core.buyer.application.services.buyer_service import BuyerService
from src.core.buyer.application.usecases import ChangeBuyerRegionUseCase, ChangeFullnameUseCase, GetCurrentBuyerUseCase
from src.core.buyer.infrastructure.adapters.region_checker import RegionCheckerAdapter
from src.core.buyer.infrastructure.buyer_unit_of_work import BuyerUnitOfWork
from src.core.buyer.infrastructure.repository import BuyerRepository


class BuyerContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    session_factory = providers.Dependency()
    region_repository = providers.Dependency()

    buyer_repository = providers.Factory(
        BuyerRepository,
        session=database_session
    )

    buyer_unit_of_work = providers.Factory(
        BuyerUnitOfWork,
        session=database_session
    )

    buyer_service = providers.Factory(
        BuyerService,
        repository=buyer_repository
    )

    region_checker_adapter = providers.Factory(
        RegionCheckerAdapter,
        repository=region_repository
    )

    change_buyer_region_usecase = providers.Factory(
        ChangeBuyerRegionUseCase,
        unit_of_work=buyer_unit_of_work,
        region_checker=region_checker_adapter
    )

    change_fullname_usecase = providers.Factory(
        ChangeFullnameUseCase,
        unit_of_work=buyer_unit_of_work
    )

    get_current_buyer_usecase = providers.Factory(
        GetCurrentBuyerUseCase,
        unit_of_work=buyer_unit_of_work
    )