from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.configuration.dependencies.container import ApplicationContainer
from src.core.references.infrastructure.repositories import (
    BrandRepository,
    CityRepository,
    ColorRepository,
    OriginCountryRepository,
)

BrandRepositoryDependency = Annotated[
    BrandRepository, Depends(Provide[ApplicationContainer.reference.brand_repository])
]

ColorRepositoryDependency = Annotated[
    ColorRepository, Depends(Provide[ApplicationContainer.reference.color_repository])
]

OriginCountryRepositoryDependency = Annotated[
    OriginCountryRepository,
    Depends(Provide[ApplicationContainer.reference.origin_country_repository]),
]

CityRepositoryDependency = Annotated[CityRepository, Depends(Provide[ApplicationContainer.reference.city_repository])]
