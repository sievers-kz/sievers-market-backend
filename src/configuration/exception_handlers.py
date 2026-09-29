# src/configuration/exception_handlers.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    AlreadyExistsError,
    DomainException,
    NotFoundError,
    RulesError,
    TooManyRequestsError,
    UnauthorizedError,
    ValidationError,
)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Регистрируем хэндлеры на базовые классы исключений.
    Любой наследник автоматически попадает в нужный хэндлер:
    AccountNotFoundError -> NotFoundError -> 404
    InvalidCredentialsError -> UnauthorizedError -> 401
    и т.д.
    """

    @app.exception_handler(TooManyRequestsError)
    async def too_many_requests_handler(request: Request, exc: TooManyRequestsError):
        logger.warning(
            "TooManyRequestsError | {} {} | {}",
            request.method,
            request.url.path,
            exc.message,
        )

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        logger.warning("NotFoundError | {} {} | {}", request.method, request.url.path, exc.message)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        logger.warning(
            "AlreadyExistsError | {} {} | {}",
            request.method,
            request.url.path,
            exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        logger.warning(
            "UnauthorizedError | {} {} | {}",
            request.method,
            request.url.path,
            exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        logger.warning(
            "ValidationError | {} {} | {}",
            request.method,
            request.url.path,
            exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(RulesError)
    async def rules_handler(request: Request, exc: RulesError):
        logger.warning("RulesError | {} {} | {}", request.method, request.url.path, exc.message)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(AccessDeniedError)
    async def access_denied_error(request: Request, exc: AccessDeniedError):
        logger.warning(
            "AccessDeniedError | {} {} | {}",
            request.method,
            request.url.path,
            exc.message,
        )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(DomainException)
    async def unexpected_error_handler(request: Request, exc: DomainException):
        logger.exception("Unexpected error | {} {}", request.method, request.url.path)

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
