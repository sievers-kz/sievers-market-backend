from src.core.shared.presentation.documentation import RouteDocs

# ===================== Brand Reference ======================

GET_ALL_BRANDS_DOC = RouteDocs(
    operation_id="getAllBrands",
    summary="Список брендов",
    description="""
        Возвращает справочник всех брендов
    """,
    responses=(),
)

GET_BRAND_BY_ID_DOC = RouteDocs(
    operation_id="getBrandById",
    summary="Бренд по ID",
    description="""
        Возвращает бренд по идентификатору
    """,
    responses=(),
)

CREATE_BRAND_DOC = RouteDocs(
    operation_id="createBrand",
    summary="Создание бренда",
    description="""
        Добавляет новый бренд в справочник
    """,
    responses=(),
)

UPDATE_BRAND_DOC = RouteDocs(
    operation_id="updateBrand",
    summary="Обновление бренда",
    description="""
        Обновляет наименование бренда
    """,
    responses=(),
)

DELETE_BRAND_DOC = RouteDocs(
    operation_id="deleteBrand",
    summary="Удаление бренда",
    description="""
        Удаляет бренд из справочника
    """,
    responses=(),
)

# ===================== Color Reference ======================

GET_ALL_COLORS_DOC = RouteDocs(
    operation_id="getAllColors",
    summary="Список цветов",
    description="""
        Возвращает справочник цветов:
        * `name` - Наименование
        * `hex` - HEX-код цвета
    """,
    responses=(),
)

GET_COLOR_BY_ID_DOC = RouteDocs(
    operation_id="getColorById",
    summary="Цвет по ID",
    description="""
        Возвращает цвет по ID
    """,
    responses=(),
)

CREATE_COLOR_DOC = RouteDocs(
    operation_id="createColor",
    summary="Создание цвета",
    description="""
        Создает новый цвет в справочнике
    """,
    responses=(),
)

UPDATE_COLOR_DOC = RouteDocs(
    operation_id="updateColor",
    summary="Обновление цвета",
    description="""
        Обновляет информацию указанного цвета:
        * `name` - Новое имя
        * `hex` - Новый HEX-код
    """,
    responses=(),
)

DELETE_COLOR_DOC = RouteDocs(
    operation_id="deleteColor",
    summary="Удаление цвета",
    description="""
        Удаляет цвет из справочника
    """,
    responses=(),
)

# ===================== Origin Country Reference ======================

GET_ALL_ORIGIN_COUNTRIES_DOC = RouteDocs(
    operation_id="getAllOriginCountries",
    summary="Список стран происхождения",
    description="""
        Возвращает справочник всех стран происхождения
    """,
    responses=(),
)

GET_ORIGIN_COUNTRY_BY_ID_DOC = RouteDocs(
    operation_id="getOriginCountryById",
    summary="Страна происхождения по ID",
    description="""
        Возвращает страну происхождения по идентификатору
    """,
    responses=(),
)

CREATE_ORIGIN_COUNTRY_DOC = RouteDocs(
    operation_id="createOriginCountry",
    summary="Создание страны происхождения",
    description="""
        Добавляет новую страну происхождения в справочник
    """,
    responses=(),
)

UPDATE_ORIGIN_COUNTRY_DOC = RouteDocs(
    operation_id="updateOriginCountry",
    summary="Обновление страны происхождения",
    description="""
        Обновляет наименование страны происхождения
    """,
    responses=(),
)

DELETE_ORIGIN_COUNTRY_DOC = RouteDocs(
    operation_id="deleteOriginCountry",
    summary="Удаление страны происхождения",
    description="""
        Удаляет страну происхождения из справочника
    """,
    responses=(),
)

# ===================== City Reference ======================

GET_ALL_CITIES_DOC = RouteDocs(
    operation_id="getAllCities",
    summary="Список городов",
    description="""
        Возвращает справочник всех городов
    """,
    responses=(),
)

GET_CITY_BY_ID_DOC = RouteDocs(
    operation_id="getCityById",
    summary="Город по ID",
    description="""
        Возвращает город по идентификатору
    """,
    responses=(),
)

CREATE_CITY_DOC = RouteDocs(
    operation_id="createCity",
    summary="Создание города",
    description="""
        Добавляет новый город в справочник
    """,
    responses=(),
)

UPDATE_CITY_DOC = RouteDocs(
    operation_id="updateCity",
    summary="Обновление города",
    description="""
        Обновляет наименование города
    """,
    responses=(),
)

DELETE_CITY_DOC = RouteDocs(
    operation_id="deleteCity",
    summary="Удаление города",
    description="""
        Удаляет город из справочника
    """,
    responses=(),
)
