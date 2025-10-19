from src.core.shared.application.exceptions.base_exception import BaseApplicationError


class InfrastructureLayerError(BaseApplicationError):
    pass


class UnitOfWorkError(InfrastructureLayerError):
    pass


class DatabaseConnectionError(UnitOfWorkError):
    pass


# ===========================================================
# EMAIL SENDERS ERRORS
# ===========================================================


class EmailSenderError(InfrastructureLayerError):
    pass


class EmailSenderRequestsError(EmailSenderError):
    pass


class EmailSenderConfigurationError(EmailSenderError):
    pass


class PhoneNormalizerServiceError(InfrastructureLayerError):
    pass
