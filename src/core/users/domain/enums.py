import enum


class UserRoleEnum(str, enum.Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"


class BusinessTypeEnum(enum.Enum):
    IP = "ip"
    TOO = "too"


class DocumentTypeEnum(enum.Enum):
    IIN = "iin"
    BIN = "bin"


