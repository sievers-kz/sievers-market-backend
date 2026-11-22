import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.configuration.exception_handlers import setup_exception_handlers
from src.core.customer.domain.exceptions import FullnameRequiredError
from src.core.iam.domain.exceptions import (
    AccountAlreadyExistsError,
    AccountNotFoundError,
    InvalidLoginCredentialsError,
    InvalidOTPCodeError,
    InvalidPasswordError,
    OTPCooldownError,
)
from src.core.shared.domain.exceptions import AccessDeniedError


@pytest.fixture
def client_factory():
    def make(exc_cls, *args):
        app = FastAPI()
        setup_exception_handlers(app)

        @app.get("/boom")
        async def boom():
            raise exc_cls(*args)

        return TestClient(app)

    return make


@pytest.mark.parametrize(
    "exc_cls",
    [
        OTPCooldownError,  # TooManyRequestsError, 429
        AccountNotFoundError,  # NotFoundError, 404
        InvalidLoginCredentialsError,  # UnauthorizedError, 401
        InvalidPasswordError,  # ValidationError, 422
        InvalidOTPCodeError,  # RulesError, 400
        AccessDeniedError,  # AccessDeniedError, 403
        AccountAlreadyExistsError,  # ConflictError, 409
    ],
)
def test_domain_error_response_contains_error_code_and_message(client_factory, exc_cls):
    response = client_factory(exc_cls).get("/boom")

    assert response.status_code == exc_cls.status_code
    body = response.json()
    assert body["error_code"] == exc_cls.error_code
    assert body["message"] == exc_cls.message
    assert body["metadata"] == {}


def test_domain_error_response_contains_metadata(client_factory):
    response = client_factory(FullnameRequiredError, "first_name").get("/boom")

    assert response.status_code == 422
    assert response.json()["metadata"] == {"field": "first_name"}
