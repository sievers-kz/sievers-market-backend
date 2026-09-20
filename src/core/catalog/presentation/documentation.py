from src.core.shared.presentation.documentation import RouteDocs

# ===================== Attribute Groups ======================

CREATE_ATTRIBUTE_GROUP_DOC = RouteDocs(
    operation_id="createAttributeGroup",
    summary="Создание группы атрибутов",
    description="""
        Создает новую логическую группу для объединения характеристик
        (например, "Общие характеристики", "Двигатель", "Габариты")
    """,
    responses=(),
)

GET_ALL_ATTRIBUTE_GROUPS_DOC = RouteDocs(
    operation_id="getAllAttributeGroups",
    summary="Список групп атрибутов",
    description="""
        Возвращает полный список всех зарегистрированных групп атрибутов
    """,
    responses=(),
)

# ===================== Attribute Definitions ======================

CREATE_ATTRIBUTE_DEFINITION_DOC = RouteDocs(
    operation_id="createAttributeDefinition",
    summary="Создание определения атрибута",
    description="""
        Создает глобальное определение характеристики товара
        (ключ, тип данных, возможные значения/опции)
    """,
    responses=(),
)

GET_ALL_ATTRIBUTE_DEFINITIONS_DOC = RouteDocs(
    operation_id="getAllAttributeDefinitions",
    summary="Список определений атрибутов",
    description="""
        Возвращает глобальный справочник всех доступных определений атрибутов
    """,
    responses=(),
)

# ===================== Subcategory Attributes ======================

CREATE_SUBCATEGORY_ATTRIBUTE_DOC = RouteDocs(
    operation_id="createSubcategoryAttribute",
    summary="Привязка атрибута к подкатегории",
    description="""
        Связывает глобальный атрибут с конкретной подкатегорией,
        задавая группу, позицию, обязательность и флаг фильтрации
    """,
    responses=(),
)

# ===================== Rubrics ======================

CREATE_RUBRIC_DOC = RouteDocs(
    operation_id="createRubric",
    summary="Создание рубрики",
    description="""
        Создает новую верхнеуровневую рубрику каталога
    """,
    responses=(),
)

CHANGE_RUBRIC_NAME_DOC = RouteDocs(
    operation_id="changeRubricName",
    summary="Изменение наименования рубрики",
    description="""
        Обновляет название существующей рубрики
    """,
    responses=(),
)

DELETE_RUBRIC_DOC = RouteDocs(
    operation_id="deleteRubric",
    summary="Удаление рубрики",
    description="""
        Мягко удаляет рубрику из каталога (переводит в статус DELETED)
    """,
    responses=(),
)

# ===================== Categories ======================

CREATE_CATEGORY_DOC = RouteDocs(
    operation_id="createCategory",
    summary="Создание категории",
    description="""
        Создает категорию второго уровня и привязывает её к родительской рубрике
    """,
    responses=(),
)

CHANGE_CATEGORY_PARENT_DOC = RouteDocs(
    operation_id="changeCategoryParent",
    summary="Смена родительской рубрики категории",
    description="""
        Переносит категорию в другую родительскую рубрику
    """,
    responses=(),
)

CHANGE_CATEGORY_NAME_DOC = RouteDocs(
    operation_id="changeCategoryName",
    summary="Изменение наименования категории",
    description="""
        Обновляет название существующей категории
    """,
    responses=(),
)

DELETE_CATEGORY_DOC = RouteDocs(
    operation_id="deleteCategory",
    summary="Удаление категории",
    description="""
        Мягко удаляет категорию из каталога (переводит в статус DELETED)
    """,
    responses=(),
)

# ===================== Subcategories ======================

CREATE_SUBCATEGORY_DOC = RouteDocs(
    operation_id="createSubcategory",
    summary="Создание подкатегории",
    description="""
        Создает конечную подкатегорию и привязывает её к родительской категории
    """,
    responses=(),
)

CHANGE_SUBCATEGORY_PARENT_DOC = RouteDocs(
    operation_id="changeSubcategoryParent",
    summary="Смена родительской категории подкатегории",
    description="""
        Переносит подкатегорию в другую родительскую категорию
    """,
    responses=(),
)

CHANGE_SUBCATEGORY_NAME_DOC = RouteDocs(
    operation_id="changeSubcategoryName",
    summary="Изменение наименования подкатегории",
    description="""
        Обновляет название существующей подкатегории
    """,
    responses=(),
)

DELETE_SUBCATEGORY_DOC = RouteDocs(
    operation_id="deleteSubcategory",
    summary="Удаление подкатегории",
    description="""
        Мягко удаляет подкатегорию из каталога (переводит в статус DELETED)
    """,
    responses=(),
)

# ===================== Catalog Views & Query Services ======================

GET_SUBCATEGORY_FORM_DOC = RouteDocs(
    operation_id="getSubcategoryForm",
    summary="Форма характеристик подкатегории",
    description="""
        Возвращает схему полей и атрибутов, необходимых для заполнения при
        подаче/редактировании объявления в подкатегории
    """,
    responses=(),
)

GET_SUBCATEGORY_FILTERS_DOC = RouteDocs(
    operation_id="getSubcategoryFilters",
    summary="Фильтры подкатегории",
    description="""
        Возвращает список атрибутов, доступных для фильтрации товаров
        в выбранной подкатегории
    """,
    responses=(),
)

GET_CATEGORY_TREE_DOC = RouteDocs(
    operation_id="getCategoryTree",
    summary="Дерево таксономии каталога",
    description="""
        Возвращает полное вложенное дерево таксономии:
        * `Rubrics` - Рубрики
        * `Categories` - Категории
        * `Subcategories` - Подкатегории
        для отображения на витрине
    """,
    responses=(),
)
