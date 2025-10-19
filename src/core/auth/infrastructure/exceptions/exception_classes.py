# ==========================================================
# INFRASTRUCTURE LAYER ERRORS
# ==========================================================
from src.core.shared.application.exceptions.base_exception import BaseApplicationError


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
# TOKEN SERVICES ERRORS
# ===========================================================


class TokenGeneratorService(InfrastructureLayerError):
    pass


class TokenExpiredError(TokenGeneratorService):
    pass


class InvalidTokenError(TokenGeneratorService):
    pass
