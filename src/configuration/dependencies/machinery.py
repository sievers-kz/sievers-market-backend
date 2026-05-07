from dependency_injector import containers, providers

from src.core.machinery.application.usecases import CreateMachineryUseCase, GetMachineryListUseCase, \
    GetMachineryDetailUseCase, GetCustomerMachineryUseCase, ActivateMachineryUseCase, DeactivateMachineryUseCase, \
    ArchiveMachineryUseCase, DeleteMachineryUseCase, GetCustomerMachineryDetailUseCase, ChangeMachineryCategoryUseCase, \
    ChangeMachineryGeneralUseCase, ChangeOperatingHistoryUseCase, ChangeMachineryPriceUseCase, \
    ChangeMachinerySpecUseCase, ChangeMachineryDescriptionUseCase
from src.core.machinery.infrastructure.queries import MachineryQuery
from src.core.machinery.infrastructure.repository import MachineryRepository
from src.core.machinery.infrastructure.uow import MachineryUnitOfWork


class MachineryContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    subcategory_service = providers.Dependency()
    wishlist_service = providers.Dependency()
    brand_repository = providers.Dependency()

    machinery_query = providers.Factory(
        MachineryQuery,
        session=database_session,
    )

    machinery_repository = providers.Factory(
        MachineryRepository,
        session=database_session,
    )

    machinery_uow = providers.Factory(
        MachineryUnitOfWork,
        session=database_session,
    )

    create_machinery_usecase = providers.Factory(
        CreateMachineryUseCase,
        uow=machinery_uow,
        subcategory_service=subcategory_service,
        brand_repository=brand_repository
    )

    get_machinery_list_usecase = providers.Factory(
        GetMachineryListUseCase,
        query=machinery_query
    )

    get_machinery_detail_usecase = providers.Factory(
        GetMachineryDetailUseCase,
        query=machinery_query
    )

    get_customer_machinery_usecase = providers.Factory(
        GetCustomerMachineryUseCase,
        query=machinery_query
    )

    activate_machinery_usecase = providers.Factory(
        ActivateMachineryUseCase,
        uow=machinery_uow
    )

    deactivate_machinery_usecase = providers.Factory(
        DeactivateMachineryUseCase,
        uow=machinery_uow
    )

    archive_machinery_usecase = providers.Factory(
        ArchiveMachineryUseCase,
        uow=machinery_uow
    )

    delete_machinery_usecase = providers.Factory(
        DeleteMachineryUseCase,
        uow=machinery_uow
    )

    get_customer_machinery_detail_usecase = providers.Factory(
        GetCustomerMachineryDetailUseCase,
        query=machinery_query,
        wishlist_service=wishlist_service
    )

    change_machinery_category_usecase = providers.Factory(
        ChangeMachineryCategoryUseCase,
        uow=machinery_uow
    )

    change_machinery_general_usecase = providers.Factory(
        ChangeMachineryGeneralUseCase,
        uow=machinery_uow
    )

    change_operating_history_usecase = providers.Factory(
        ChangeOperatingHistoryUseCase,
        uow=machinery_uow
    )

    change_machinery_price_usecase = providers.Factory(
        ChangeMachineryPriceUseCase,
        uow=machinery_uow
    )

    change_machinery_spec_usecase = providers.Factory(
        ChangeMachinerySpecUseCase,
        uow=machinery_uow,
        subcategory_service=subcategory_service,
    )

    change_machinery_description_usecase = providers.Factory(
        ChangeMachineryDescriptionUseCase,
        uow=machinery_uow
    )
