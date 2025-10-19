from src.core.shared.application.exceptions.base_exception import BaseApplicationError


class DomainLayerError(BaseApplicationError):
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


class InvalidCredentialsError(DomainLayerError):
    pass
