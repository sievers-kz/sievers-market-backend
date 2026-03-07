from dependency_injector import containers, providers

from src.core.references.application.services.attribute import AttributeService
from src.core.references.application.services.region import RegionService
from src.core.references.application.usecases import GetSubcategoryFilterUseCase, GetSubcategoryFormUseCase, \
    GetBrandsUseCase, GetRegionsUseCase, GetCountriesUseCase, GetColorsUseCase
from src.core.references.infrastructure.filter_builder import FilterBuilderService
from src.core.references.infrastructure.form_builder import FormBuilderService
from src.core.references.infrastructure.repository import AttributeRepository, SubcategoryRepository, RegionRepository, \
    BrandRepository, CountryRepository, ColorRepository


class ReferenceContainer(containers.DeclarativeContainer):
    database_session = providers.Dependency()

    filter_builder = providers.Factory(
        FilterBuilderService
    )

    form_builder = providers.Factory(
        FormBuilderService
    )

    region_repository = providers.Factory(
        RegionRepository,
        session=database_session
    )

    attribute_repository = providers.Factory(
        AttributeRepository,
        session=database_session
    )

    subcategory_repository = providers.Factory(
        SubcategoryRepository,
        session=database_session
    )

    brand_repository = providers.Factory(
        BrandRepository,
        session=database_session
    )

    country_repository = providers.Factory(
        CountryRepository,
        session=database_session
    )

    color_repository = providers.Factory(
        ColorRepository,
        session=database_session
    )

    get_subcategory_filter_usecase = providers.Factory(
        GetSubcategoryFilterUseCase,
        repository=attribute_repository,
        filter_builder=filter_builder
    )

    get_subcategory_form_usecase = providers.Factory(
        GetSubcategoryFormUseCase,
        attribute_repository=attribute_repository,
        subcategory_repository=subcategory_repository,
        form_builder=form_builder
    )

    get_brands_usecase = providers.Factory(
        GetBrandsUseCase,
        repository=brand_repository
    )

    get_regions_usecase = providers.Factory(
        GetRegionsUseCase,
        repository=region_repository
    )

    get_countries_usecase = providers.Factory(
        GetCountriesUseCase,
        repository=country_repository
    )

    get_colors_usecase = providers.Factory(
        GetColorsUseCase,
        repository=color_repository
    )

    attribute_service = providers.Factory(
        AttributeService,
        repository=attribute_repository
    )

    region_service = providers.Factory(
        RegionService,
        repository=region_repository
    )