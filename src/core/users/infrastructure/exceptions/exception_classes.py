# ==========================================================
# INFRASTRUCTURE LAYER ERRORS
# ==========================================================
from src.base_exception import BaseApplicationError


class InfrastructureLayerError(BaseApplicationError):
    pass


# ==========================================================
# REPOSITORIES ERRORS
# ==========================================================


class RepositoryError(InfrastructureLayerError):
    pass


class UniqueConstraintError(RepositoryError):
    pass


class ResultNotFoundError(RepositoryError):
    pass


# ===========================================================
# UNIT OF WORKS ERRORS
# ===========================================================


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


# ===========================================================
# TOKEN SERVICES ERRORS
# ===========================================================


class TokenGeneratorService(InfrastructureLayerError):
    pass


class TokenExpiredError(TokenGeneratorService):
    pass


class InvalidTokenError(TokenGeneratorService):
    pass


# ===========================================================
# TOKEN SERVICES ERRORS
# ===========================================================


class PhoneNormalizerServiceError(InfrastructureLayerError):
    pass
