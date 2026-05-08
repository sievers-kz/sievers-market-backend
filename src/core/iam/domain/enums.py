import enum


class UserRole(str, enum.Enum):
    BUYER = "customer"
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


class OTPType(str, enum.Enum):
    CONFIRMATION = "confirmation"
    PASSWORD_RESET = "password_reset"
    CHANGE_EMAIL = "change_email"
    CHANGE_PHONE = "change_phone"

