from dependency_injector import containers, providers

from src.core.references.infrastructure.models import Brand, City, Color, OriginCountry
from src.core.references.infrastructure.repositories import (
    BrandRepository,
    CityRepository,
    ColorRepository,
    OriginCountryRepository,
)


class ReferenceContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    database_session = providers.Dependency()

    brand_repository = providers.Factory(BrandRepository, model=Brand, session=database_session)
    color_repository = providers.Factory(ColorRepository, model=Color, session=database_session)
    origin_country_repository = providers.Factory(
        OriginCountryRepository, model=OriginCountry, session=database_session
    )
    city_repository = providers.Factory(CityRepository, model=City, session=database_session)
