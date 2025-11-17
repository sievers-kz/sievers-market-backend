import datetime

import pytest
import random
import uuid

import pytest_asyncio
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import NullPool, event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.api.auth.auth_dto import UserCredentialsDTO, AuthTokenDTO, UserIdentityDTO
from src.configuration.database.connection import Base
from src.configuration.dependencies.depends import DependencyContainer

from src.api.users.user_dto import CreateUserDTO, UserProfileDTO, BusinessDetailsDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.factories import UserIdentityFactory
from src.core.users.domain.entities import BusinessDetails, UserProfile
from src.core.users.domain.enums import UserRoleEnum, DocumentTypeEnum, BusinessTypeEnum
from src.core.users.domain.value_objects import Fullname
from src.core.users.infrastructure.factories import UserFactory


class TestDatabaseConnectionSettings(BaseSettings):
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_NAME: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASS: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    EMAIL_TOKEN_LIFETIME: int
    PASSWORD_RESET_TOKEN_LIFETIME: int

    SEND_GRID_API_KEY: str
    FROM_EMAIL: str
    EMAIL_CONFIRMATION_TEMPLATE_ID: str
    PASSWORD_RESET_TEMPLATE_ID: str

    @computed_field(return_type=str)
    @property
    def test_database_url(self):
        return (
            f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:"
            f"{self.TEST_POSTGRES_PASS}@{self.TEST_POSTGRES_HOST}:"
            f"{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env.test")


@pytest.fixture(scope="session")
def test_settings() -> TestDatabaseConnectionSettings:
    return TestDatabaseConnectionSettings()


@pytest_asyncio.fixture(scope="session")
async def engine(test_settings):
    async_engine = create_async_engine(
        url=test_settings.test_database_url,
        echo=False,
        poolclass=NullPool
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session_factory(engine):
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )


@pytest_asyncio.fixture(scope="function")
async def database_session(session_factory):
    """
    Возвращает готовый session из sessionmaker
    """
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def container(engine, session_factory, test_settings):
    container = DependencyContainer()
    container.config.from_pydantic(test_settings)

    container.async_engine.override(engine)
    container.async_session_maker.override(session_factory)

    yield container


@pytest.fixture(scope="function")
def create_user_dto():
    """
    Глобальная фабрика для создания CreateUserDTO.
    По умолчанию создает INDIVIDUAL, если не указано иное.
    """
    def _factory(
        role: UserRoleEnum = UserRoleEnum.INDIVIDUAL,
        email: str = None,
        phone: str = None,
        doc_value: str = None,
        business_type: BusinessTypeEnum = BusinessTypeEnum.IP,
        document_type: DocumentTypeEnum = DocumentTypeEnum.IIN,
        credentials: str = None
    ):
        default_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        defailt_phone = f"8747{random.randint(1000000, 9999999)}"
        default_doc_value = f"123456{random.randint(100000, 999999)}"

        business_details = None
        if role == UserRoleEnum.BUSINESS:
            business_details = BusinessDetailsDTO(
                business_type=business_type,
                organization_fullname="BEST AGROW",
                document_type=document_type,
                document_value=doc_value or default_doc_value
            )

        profile = UserProfileDTO(
            last_name="Бисенов",
            first_name="Мейржан",
            patronymic="Баскарович",
            avatar_url="my_avatar"
        )

        default_credentials = UserCredentialsDTO(raw_password="supersecret")

        return CreateUserDTO(
            role=role,
            email=email or default_email,
            phone=phone or defailt_phone,
            profile=profile,
            credentials=credentials or default_credentials,
            business_details=business_details
        )

    return _factory


@pytest.fixture(scope="function")
def create_domain_user_from_dto(create_user_dto):
    """
    Глобальная фабрика для создания CreateUserDTO.
    По умолчанию создает INDIVIDUAL, если не указано иное.
    """
    def _factory(**kwargs):
        dto = create_user_dto(**kwargs)

        return UserFactory.create(dto)

    return _factory


@pytest.fixture(scope="function")
def create_domain_user_identity_from_dto(create_user_dto):
    """
    Возвращает (user, identity).
    Берёт credentials из DTO (create_user_dto), а не из User.
    """
    def _factory(user_id: uuid.UUID, **kwargs):
        dto = create_user_dto(**kwargs)

        token = AuthTokenDTO(
            token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN,
            token_value=str(uuid.uuid4()),
            is_revoked=False,
            expires_at=datetime.datetime.utcnow(),
        )

        credentials = dto.credentials
        if credentials is None:
            credentials = UserCredentialsDTO(raw_password="supersecret")

        identity = UserIdentityFactory.create(
            user_id=user_id,
            credentials=credentials,
            tokens=[token]
        )

        return identity

    return _factory
