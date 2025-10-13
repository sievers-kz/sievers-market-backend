from src.base_exception import BaseApplicationError


class DomainLayerError(BaseApplicationError):
    pass


class UserAlreadyExistsError(DomainLayerError):
    pass


class InvalidInputError(DomainLayerError):
    pass


class MissingRequiredFieldError(DomainLayerError):
    pass


class InvalidCredentialsError(DomainLayerError):
    pass


# ==========================================================
# EMAIL CONFIRMATION ERRORS
# ==========================================================


class EmailNotConfirmedError(DomainLayerError):
    pass


class InvalidEmailConfirmationCodeError(DomainLayerError):
    pass


class ConfirmationCodeExpiredError(DomainLayerError):
    pass


class EmailAlreadyConfirmedError(DomainLayerError):
    pass


# ==========================================================
# TOKENS ERRORS
# ==========================================================


class TokenAlreadyRevokedError(DomainLayerError):
    pass


class TokenCryptographyError(DomainLayerError):
    pass


class TokenStateError(DomainLayerError):
    pass
