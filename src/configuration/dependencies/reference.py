from dependency_injector import containers, providers

from src.core.references.infrastructure.repositories.brand import BrandRepository
from src.core.references.infrastructure.repositories.city import CityRepository
from src.core.references.infrastructure.repositories.color import ColorRepository
from src.core.references.infrastructure.repositories.country import CountryRepository
from src.core.references.infrastructure.repositories.region import RegionRepository


class ReferenceContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    brand_repository = providers.Factory(BrandRepository, session=database_session)
    color_repository = providers.Factory(ColorRepository, session=database_session)
    country_repository = providers.Factory(CountryRepository, session=database_session)
    region_repository = providers.Factory(RegionRepository, session=database_session)
    city_repository = providers.Factory(CityRepository, session=database_session)
