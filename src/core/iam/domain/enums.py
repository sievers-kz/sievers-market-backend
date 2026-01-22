import enum


class UserRole(str, enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"

    @property
    def label(self):
        labels = {
            UserRole.BUYER: "Покупатель",
            UserRole.SELLER: "Продавец",
            UserRole.ADMIN: "Администратор"
        }
        return labels.get(self, "Неизвестный тип роли")


class TokenType(str, enum.Enum):
    REFRESH = "refresh"
    ACCESS = "access"
    EMAIL = "email"
    PASSWORD = "password"
