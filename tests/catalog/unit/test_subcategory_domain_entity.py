from uuid import uuid4

import pytest

from src.core.catalog.domain.entities import Subcategory
from src.core.catalog.domain.value_objects import Attribute
from src.core.catalog.infrastructure.enums import AttributeType, CatalogStatus
from src.core.catalog.infrastructure.exceptions import DuplicateAttributeError


@pytest.fixture
def sample_attributes():
    return [
        Attribute(
            key="engine_power",
            label="Мощность",
            type=AttributeType.INTEGER,
            required=True,
        ),
        Attribute(
            key="color",
            label="Цвет",
            type=AttributeType.ENUMERATE,
            options=["Красный", "Зеленый"],
        ),
        Attribute(
            key="is_new", label="Новый?", type=AttributeType.BOOLEAN, required=False
        ),
    ]


@pytest.fixture
def active_subcategory(sample_attributes):
    return Subcategory.create(
        category_id=uuid4(), name="Тракторы", attributes=sample_attributes
    )


def test_subcategory_create_success(sample_attributes):
    category_id = uuid4()
    name = "Комбайны"

    subcategory = Subcategory.create(
        category_id=category_id, name=name, attributes=sample_attributes
    )

    assert subcategory.id is not None
    assert subcategory.category_id == category_id
    assert subcategory.name == name
    assert subcategory.status == CatalogStatus.ACTIVE
    assert subcategory.attributes == sample_attributes


def test_change_name_success(active_subcategory):
    active_subcategory.change_name("Новое имя тракторов")
    assert active_subcategory.name == "Новое имя тракторов"


def test_change_name_ignore_if_same(active_subcategory):
    active_subcategory.change_name("Тракторы")
    assert active_subcategory.name == "Тракторы"


def test_change_parent_clears_attributes(active_subcategory):
    new_parent_id = uuid4()

    active_subcategory.change_parent(new_parent_id)

    assert active_subcategory.category_id == new_parent_id
    assert active_subcategory.attributes == []


def test_change_parent_ignore_if_same(active_subcategory, sample_attributes):
    current_parent_id = active_subcategory.category_id

    active_subcategory.change_parent(current_parent_id)

    assert active_subcategory.category_id == current_parent_id
    assert active_subcategory.attributes == sample_attributes


def test_replace_attributes_success(active_subcategory):
    new_attrs = [Attribute(key="weight", label="Вес", type=AttributeType.FLOAT)]

    active_subcategory.replace_attributes(new_attrs)
    assert active_subcategory.attributes == new_attrs


def test_replace_attributes_raises_error_on_duplicates(active_subcategory):
    duplicated_attrs = [
        Attribute(key="volume", label="Объем", type=AttributeType.INTEGER),
        Attribute(key="volume", label="Объем", type=AttributeType.INTEGER),
    ]

    with pytest.raises(DuplicateAttributeError):
        active_subcategory.replace_attributes(duplicated_attrs)


def test_validate_attributes_happy_path(active_subcategory):
    user_input = {
        "engine_power": "120",
        "color": "Красный",
        "is_new": "true",
        "hacker_garbage": "attack",
    }

    clean_data = active_subcategory.validate_attributes(user_input)

    assert clean_data["engine_power"] == 120
    assert clean_data["color"] == "Красный"
    assert clean_data["is_new"] is True
    assert "hacker_garbage" not in clean_data


def test_validate_attributes_skips_optional_missing_fields(active_subcategory):
    user_input = {"engine_power": 80, "color": "Зеленый"}

    clean_data = active_subcategory.validate_attributes(user_input)

    assert "is_new" not in clean_data
    assert clean_data["engine_power"] == 80


def test_delete_subcategory_success(active_subcategory):
    active_subcategory.delete()
    assert active_subcategory.status == CatalogStatus.DELETED


def test_delete_already_deleted_subcategory_noop(active_subcategory):
    active_subcategory.delete()
    assert active_subcategory.status == CatalogStatus.DELETED

    active_subcategory.delete()
    assert active_subcategory.status == CatalogStatus.DELETED
