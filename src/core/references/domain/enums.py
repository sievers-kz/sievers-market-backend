import enum
from enum import Enum


class AttrValueType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    ENUM = "enum"


class WidgetType(str, Enum):
    RANGE = "range"
    SELECT = "select"
    NUMBER = "number"
    SWITCH = "switch"
    TEXT = "text"
