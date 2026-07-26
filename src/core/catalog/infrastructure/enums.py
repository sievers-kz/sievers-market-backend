from enum import Enum


class AttributeType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    ENUMERATE = "enumerate"
    REFERENCE = "reference"


class CatalogStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
