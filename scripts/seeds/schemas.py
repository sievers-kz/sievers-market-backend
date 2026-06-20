from src.core.catalog.presentation.dto.subcategory import Attribute
from src.core.shared.presentation.dto import DTO


class SubcategorySeed(DTO):
    name: str
    attributes: list[Attribute]


class CategorySeed(DTO):
    name: str
    subcategories: list[SubcategorySeed]


class RubricSeed(DTO):
    name: str
    attributes: list[Attribute] = []
    categories: list[CategorySeed]


class BrandSeed(DTO):
    name: str


class ColorSeed(DTO):
    name: str
    hex: str


class RegionSeed(DTO):
    name: str
    cities: list[str]


class CountrySeed(DTO):
    name: str
