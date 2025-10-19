import enum


class TokenTypeEnum(enum.Enum):
    REFRESH_TOKEN = "refresh_token"
    ACCESS_TOKEN = "access_token"
    EMAIL_CONFIRMATION_TOKEN = "email_confirmation_token"
    PASSWORD_RESET_TOKEN = "password_reset_token"
