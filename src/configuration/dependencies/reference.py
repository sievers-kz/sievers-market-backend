from dependency_injector import containers, providers

from src.core.references.application.services import BrandService, ColorService
from src.core.references.infrastructure.repositories import (
    BrandRepository,
    ColorRepository,
)
from src.core.references.infrastructure.uow import ReferenceUnitOfWork


class ReferenceContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    brand_repository = providers.Factory(BrandRepository, session=database_session)

    color_repository = providers.Factory(ColorRepository, session=database_session)

    reference_unit_of_work = providers.Factory(
        ReferenceUnitOfWork, session_factory=session_factory
    )

    brand_service = providers.Factory(BrandService, uow=reference_unit_of_work)

    color_service = providers.Factory(ColorService, uow=reference_unit_of_work)
