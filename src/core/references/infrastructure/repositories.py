from src.core.references.infrastructure.models import Brand, City, Color, OriginCountry
from src.core.shared.infrastructure.generic_repository import GenericRepository


class BrandRepository(GenericRepository[Brand]):
    pass


class ColorRepository(GenericRepository[Color]):
    pass


class CityRepository(GenericRepository[City]):
    pass


class OriginCountryRepository(GenericRepository[OriginCountry]):
    pass
