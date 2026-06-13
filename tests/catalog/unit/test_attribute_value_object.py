import pytest

from src.core.catalog.domain.enums import AttributeType
from src.core.catalog.domain.exceptions import (
    AttributeOptionError,
    AttributeRequiredError,
    AttributeTypeError,
)
from src.core.catalog.domain.value_objects import Attribute


@pytest.mark.parametrize(
    "attr_type, raw_value, expected_value",
    [
        (AttributeType.INTEGER, "15", 15),
        (AttributeType.INTEGER, 42, 42),
        (AttributeType.FLOAT, "12.5", 12.5),
        (AttributeType.FLOAT, 10, 10.0),
        (AttributeType.BOOLEAN, "True", True),
        (AttributeType.BOOLEAN, "1", True),
        (AttributeType.BOOLEAN, "yes", True),
        (AttributeType.BOOLEAN, "false", False),
        (AttributeType.STRING, 100, "100"),
        (AttributeType.STRING, "нормально", "нормально"),
    ],
)
def test_attribute_cast_type_success(attr_type, raw_value, expected_value):
    attr = Attribute(key="test_key", label="Тест", type=attr_type)
    assert attr.validate_value(raw_value) == expected_value


def test_attribute_enumerate_success():
    attr = Attribute(
        key="color",
        label="Цвет",
        type=AttributeType.ENUMERATE,
        options=["Синий", "Красный", "Зеленый"],
    )
    assert attr.validate_value("Синий") == "Синий"


def test_attribute_enumerate_invalid_option_raises_error():
    attr = Attribute(
        key="color",
        label="Цвет",
        type=AttributeType.ENUMERATE,
        options=["Синий", "Красный"],
    )
    with pytest.raises(AttributeOptionError):
        attr.validate_value("Зеленый")  # Такого цвета нет в списке


@pytest.mark.parametrize("invalid_value", [None, ""])
def test_required_attribute_raises_error_on_empty(invalid_value):
    attr = Attribute(
        key="power", label="Мощность", type=AttributeType.INTEGER, required=True
    )
    with pytest.raises(AttributeRequiredError):
        attr.validate_value(invalid_value)


def test_not_required_attribute_returns_none_on_empty():
    attr = Attribute(
        key="power", label="Мощность", type=AttributeType.INTEGER, required=False
    )
    assert attr.validate_value(None) is None


@pytest.mark.parametrize(
    "attr_type, bad_value",
    [
        (AttributeType.INTEGER, "не число"),
        (AttributeType.INTEGER, [1, 2]),
        (AttributeType.FLOAT, "abc"),
    ],
)
def test_attribute_invalid_type_raises_error(attr_type, bad_value):
    attr = Attribute(key="test_key", label="Тест", type=attr_type)
    with pytest.raises(AttributeTypeError):
        attr.validate_value(bad_value)


def test_attribute_serialization_cycle():
    raw_data = {
        "key": "engine_volume",
        "label": "Объем двигателя",
        "type": "float",
        "required": True,
        "filterable": True,
        "unit": "л.с.",
        "options": None,
        "position": 1,
    }

    attr = Attribute.from_dict(raw_data)
    assert attr.key == "engine_volume"
    assert attr.type == AttributeType.FLOAT
    assert attr.required is True

    serialized = attr.to_dict()
    assert serialized["key"] == "engine_volume"
    assert serialized["type"] == AttributeType.FLOAT
    assert serialized["position"] == 1
