from enum import Enum


class Kind(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
