# ========================================================
# APPLICATION LAYER ERRORS
# ========================================================
from src.core.shared.application.exceptions.base_exception import BaseApplicationError


class ApplicationLayerError(BaseApplicationError):
    pass


# ========================================================
# INTERNAL SERVER ERRORS (500)
# ========================================================


class InternalServerError(ApplicationLayerError):
    pass


# ========================================================
# SERVICE AVAILABILITY ERRORS (503)
# ========================================================


class ServiceUnavailableError(ApplicationLayerError):
    pass
