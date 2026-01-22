from dependency_injector import containers, providers

from src.core.machinery.application.usecases import (
    CreateMachineryUseCase,
    ActivateMachineryUseCase,
    DeactivateMachineryUseCase, UpdateMachineryUseCase, DeleteMachineryUseCase, FilterMachineryUseCase,
    GetSellerMachineryUseCase, GetDetailMachineryUseCase, GetOwnerDetailMachineryUseCase
)

from src.core.machinery.infrastructure.adapters import AttributeValidator
from src.core.machinery.infrastructure.machinery_unit_of_work import MachineryUnitOfWork
from src.core.machinery.infrastructure.repository import MachineryRepository, MachineryReader


class MachineryContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()
    attribute_service = providers.Dependency()

    machinery_repository = providers.Factory(
        MachineryRepository,
        session=database_session
    )

    machinery_reader = providers.Factory(
        MachineryReader,
        session=database_session
    )

    machinery_unit_of_work = providers.Factory(
        MachineryUnitOfWork,
        session=database_session
    )

    attribute_validator = providers.Factory(
        AttributeValidator,
        attribute_service=attribute_service
    )

    create_machinery_usecase = providers.Factory(
        CreateMachineryUseCase,
        unit_of_work=machinery_unit_of_work,
        attribute_validator=attribute_validator
    )

    update_machinery_usecase = providers.Factory(
        UpdateMachineryUseCase,
        unit_of_work=machinery_unit_of_work,
        attribute_validator=attribute_validator
    )

    activate_machinery_usecase = providers.Factory(
        ActivateMachineryUseCase,
        unit_of_work=machinery_unit_of_work
    )

    deactivate_machinery_usecase = providers.Factory(
        DeactivateMachineryUseCase,
        unit_of_work=machinery_unit_of_work
    )

    delete_machinery_usecase = providers.Factory(
        DeleteMachineryUseCase,
        unit_of_work=machinery_unit_of_work
    )

    filter_machinery_usecase = providers.Factory(
        FilterMachineryUseCase,
        machinery_reader=machinery_reader
    )

    get_seller_machinery_usecase = providers.Factory(
        GetSellerMachineryUseCase,
        reader=machinery_reader
    )

    get_detail_machinery_usecase = providers.Factory(
        GetDetailMachineryUseCase,
        reader=machinery_reader
    )

    get_owner_detail_machinery_usecase = providers.Factory(
        GetOwnerDetailMachineryUseCase,
        reader=machinery_reader
    )