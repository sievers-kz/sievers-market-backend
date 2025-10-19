from src.core.shared.application.exceptions.base_exception import BaseApplicationError


class DomainLayerError(BaseApplicationError):
    pass


class UserAlreadyExistsError(DomainLayerError):
    pass


class InvalidInputError(DomainLayerError):
    pass


class MissingRequiredFieldError(DomainLayerError):
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






