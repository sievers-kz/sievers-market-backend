import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from src.core.iam.presentation.dto import CreateUserRequest
from src.core.iam.domain.entities import Account, Token
from src.core.iam.domain.enums import TokenType
from src.core.iam.domain.value_objects import Email, Phone, Password
from src.core.shared.application.interfaces.queue_service import IQueueService


def create_domain_account(
    is_active: bool | None = False,
    tokens: list | None = None
) -> Account:
    return Account(
        id=uuid.uuid4(),
        email=Email("test@example.com"),
        phone=Phone("+77472006243"),
        password=Password("$2b$12$fakehashstring..."),
        is_active=is_active,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        tokens=tokens if tokens is not None else []
    )


def create_user_request() -> CreateUserRequest:
    return CreateUserRequest(
        email="test@example.com",
        raw_password="super_secret",
        last_name="Test",
        first_name="Test",
    )


@pytest.fixture
def mock_arq(container):
    mock = AsyncMock(spec=IQueueService)
    container.shared.arq_service.override(mock)
    return mock


def get_token_by_type(tokens: list, target_type: TokenType):
    return next((t for t in tokens if t.type == target_type), None)


def get_token_by_value(tokens: list, target_value: str):
    return next((t for t in tokens if t.value == target_value), None)


@pytest_asyncio.fixture
async def password_hasher(container):
    return container.iam.bcrypt_password_hasher()


@pytest_asyncio.fixture
async def token_service(container):
    return container.iam.pyjwt_token_service()


@pytest_asyncio.fixture
async def create_user_usecase(container, mock_arq):
    return await container.iam.create_user_usecase()


@pytest_asyncio.fixture
async def account_confirmation_usecase(container):
    return await container.iam.account_confirmation_usecase()


@pytest_asyncio.fixture
async def resend_confirmation_code_usecase(container):
    return await container.iam.resend_confirmation_code_usecase()


@pytest_asyncio.fixture
async def login_user_usecase(container):
    return await container.iam.login_user_usecase()


@pytest_asyncio.fixture
async def logout_user_usecase(container):
    return await container.iam.logout_user_usecase()


@pytest_asyncio.fixture
async def refresh_token_usecase(container):
    return await container.iam.refresh_token_usecase()


@pytest_asyncio.fixture
async def forgot_password_usecase(container):
    return await container.iam.forgot_password_usecase()


@pytest_asyncio.fixture
async def reset_password_usecase(container):
    return await container.iam.reset_password_usecase()


@pytest_asyncio.fixture
async def change_password_usecase(container):
    return await container.iam.change_password_usecase()


@pytest_asyncio.fixture
async def account_repository(container):
    return await container.iam.account_repository()


@pytest.fixture
def redis_service(container):
    return container.shared.redis_service()
