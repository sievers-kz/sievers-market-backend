from enum import Enum


class Kind(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"


class RegistryStatus(str, Enum):
    VERIFIED = "verified"
    PENDING = "pending"
    NOT_FOUND = "not_found"


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
