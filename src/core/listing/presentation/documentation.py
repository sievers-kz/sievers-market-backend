from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.customer.domain.exceptions import (
    OrganizationCannotPublishError,
    OrganizationNotFoundError,
    OrganizationProfileIncompleteError,
)
from src.core.listing.domain.exceptions import (
    ListingAttributeFilterWithoutSubcategoryError,
    ListingDeletedError,
    ListingInvalidFilterKeyError,
    ListingInvalidRangeFilterError,
    ListingNotFoundError,
)
from src.core.shared.presentation.documentation import RouteDocs

CREATE_LISTING_DOC = RouteDocs(
    operation_id="createListing",
    summary="Создание объявления",
    description="""
        Создаёт новое объявление со статичными полями, галереей и динамическими атрибутами подкатегории.

        Объявление размещается от имени организации из `organization_id`. Организация должна принадлежать
        текущему покупателю (иначе `404`) и быть подтверждённой в реестре, `registry_status: verified`
        (иначе `403`). Список организаций для выбора — `GET /api/v1/customer/organizations`.

        Категория должна существовать, а подкатегория — принадлежать этой категории, иначе `404`
        `catalog_not_found_error` (`metadata.field` — id не найденного объекта). Подкатегория без
        заданных атрибутов допустима.
    """,
    responses=(
        OrganizationNotFoundError,
        CatalogNotFoundError,
        OrganizationCannotPublishError,
        OrganizationProfileIncompleteError,
    ),
)

CHANGE_LISTING_PRICE_DOC = RouteDocs(
    operation_id="changeListingPrice",
    summary="Изменение цены объявления",
    description="""
        Обновляет цену и валюту объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_LOCATION_DOC = RouteDocs(
    operation_id="changeListingLocation",
    summary="Изменение локации объявления",
    description="""
        Обновляет город объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_DESCRIPTION_DOC = RouteDocs(
    operation_id="changeListingDescription",
    summary="Изменение описания объявления",
    description="""
        Обновляет текстовое описание объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_ATTRIBUTE_DOC = RouteDocs(
    operation_id="changeListingAttribute",
    summary="Изменение атрибутов объявления",
    description="""
        Обновляет значения динамических атрибутов объявления в рамках подкатегории.

        `subcategory_id` должен совпадать с подкатегорией объявления, иначе `404` `catalog_not_found_error`.
    """,
    responses=(
        ListingNotFoundError,
        CatalogNotFoundError,
    ),
)

ACTIVATE_LISTING_DOC = RouteDocs(
    operation_id="activateListing",
    summary="Публикация объявления",
    description="""
        Переводит объявление в статус `active` — делает его видимым в публичном каталоге.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

DEACTIVATE_LISTING_DOC = RouteDocs(
    operation_id="deactivateListing",
    summary="Снятие объявления с публикации",
    description="""
        Переводит объявление в статус `inactive` — скрывает из каталога без удаления.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

ARCHIVE_LISTING_DOC = RouteDocs(
    operation_id="archiveListing",
    summary="Архивация объявления",
    description="""
        Переводит объявление в статус `archived`.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

DELETE_LISTING_DOC = RouteDocs(
    operation_id="deleteListing",
    summary="Удаление объявления",
    description="""
        Переводит объявление в статус `deleted` (мягкое удаление).
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

SEARCH_LISTING_DOC = RouteDocs(
    operation_id="searchListing",
    summary="Поиск объявлений",
    description="""
        Поиск и фильтрация активных объявлений. Возвращает те же карточки, что `getListingsCatalog`.

        Фильтры: `text` (название, описание), `category_id`, `subcategory_id`, `city_id`, `price_min`,
        `price_max` и `attributes` (ключ атрибута → значение, равенство). Фильтр по `attributes` работает
        только вместе с `subcategory_id` и только по атрибутам, фильтруемым в этой подкатегории
        (см. `getFilterableAttributes`); иначе `422`.

        `attribute_ranges`: диапазоны для числовых атрибутов (`integer`, `float`), например
        `{"year_of_issue": {"min": 2015, "max": 2020}}`; можно одну границу. Те же правила, что у
        `attributes`, плюс атрибут должен быть числовым (иначе `422 listing_invalid_range_filter_error`).

        Цена: `price_min`, `price_max` и сортировка по цене пока работают только среди объявлений в тенге
        (`KZT`); объявления в других валютах при этом не попадают в выдачу. Без фильтра и сортировки по цене
        видны все.

        Сортировка `sort`: `newest`, `price_asc`, `price_desc`. Без `sort` при заданном `text` порядок по
        релевантности, без `text` сначала новые. `page` от 1, `limit` от 1 до 50.

        На странице может прийти меньше `limit` карточек, если объявление стало неактивным после индексации.
    """,
    responses=(
        ListingAttributeFilterWithoutSubcategoryError,
        ListingInvalidFilterKeyError,
        ListingInvalidRangeFilterError,
    ),
)

GET_LISTINGS_CATALOG_DOC = RouteDocs(
    operation_id="getListingsCatalog",
    summary="Список объявлений каталога",
    description="""
        Возвращает постраничный список карточек объявлений по категории/подкатегории, сначала новые.
        В карточке: дата создания (`created_at`), название организации-продавца (`organization_name`:
        название магазина или, если его нет, юридическое название) и состояние (`condition`: `new` или `used`;
        `null`, если у подкатегории нет такого атрибута).
    """,
    responses=(),
)

GET_MY_LISTINGS_DOC = RouteDocs(
    operation_id="getMyListings",
    summary="Мои объявления",
    description="""
        Возвращает постраничный список объявлений всех организаций текущего покупателя (кабинет).

        Читает из базы, а не из поискового индекса, поэтому видны и неактивные объявления. Удалённые не
        возвращаются. Без `status` приходят активные, неактивные и архивные.

        Фильтры: `status` (`active`, `inactive`, `archived`), `organization_id` (организация должна
        принадлежать текущему покупателю, иначе `404`), `category_id`. Сортировка `sort`: `newest`
        (по умолчанию) или `oldest` по дате создания. `limit` от 1 до 50.

        `preview_image` и `city` могут быть `null` (нет фото или города).
    """,
    responses=(OrganizationNotFoundError,),
)

GET_LISTING_DETAILS_DOC = RouteDocs(
    operation_id="getListingDetails",
    summary="Детали объявления",
    description="""
        Возвращает полную карточку активного объявления.

        - `seller`: организация-продавец. Юрданные открыто (наименование, `kind` и `tax_id`: ИИН у ИП,
          БИН у компании, адрес, проверка по реестру). Телефон и email только маской (`phone_masked`,
          `email_masked`): полные значения отдаёт `GET /listing/{listing_id}/contacts`.
        - `specs`: характеристики, готовые к показу, по группам и в порядке формы. Для вариантов
          отдаётся подпись («Б/У»), для справочников название («John Deere»), для булевых «Да»/«Нет»,
          числа как есть, единица измерения в `unit`. Пустые значения не попадают.
        - `condition`: ключ варианта состояния (`new`, `used`) или `null`.
        - `attributes`: сырые значения, как их сохранил продавец (для формы редактирования).

        Неактивное, удалённое или несуществующее объявление: 404.
    """,
    responses=(ListingNotFoundError,),
)


GET_LISTING_CONTACTS_DOC = RouteDocs(
    operation_id="getListingContacts",
    summary="Контакты продавца",
    description="""
        Полные телефон и email продавца для кнопки «Показать контакты». Без авторизации.

        В детальной карточке контакты только маской, чтобы их не было в HTML страницы.
        Поле `null`, если продавец его не указал.

        Неактивное, удалённое или несуществующее объявление: 404.
    """,
    responses=(ListingNotFoundError,),
)
