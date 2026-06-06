from enum import Enum


class AttributeType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    ENUMERATE = "enumerate"
    REFERENCE = "reference"


class WidgetType(str, Enum):
    RANGE = "range"
    NUMBER = "number"
    TEXT = "text"
    CHECKBOX = "checkbox"
    SELECT = "select"
    SWITCH = "switch"


class CatalogStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"

