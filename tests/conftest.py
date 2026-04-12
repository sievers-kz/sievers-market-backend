import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from fixtures.seed import DataSeeder
from src.configuration.database.connection import Base
from src.configuration.dependencies.container import ApplicationContainer
from src.configuration.settings.settings import ApplicationSettings
from src.main import create_fastapi_app


pytest_plugins = [
    "tests.iam.conftest",
    "tests.customer.conftest",
    "tests.machinery.conftest"
]


@pytest.fixture(scope="session")
def test_settings() -> ApplicationSettings:
    return ApplicationSettings()


@pytest_asyncio.fixture(scope="session")
async def test_engine(test_settings: ApplicationSettings):
    if test_settings.mode != "test":
        pytest.exit(f"СТОП! Попытка запустить тесты на рабочей БД: {test_settings.database.name}")

    async_engine = create_async_engine(
        url=test_settings.database.database_url,
        echo=False,
        poolclass=NullPool
    )

    yield async_engine
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        seeder = DataSeeder(session=session)
        await seeder.seed_all()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session_factory(test_engine):
    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        await conn.begin_nested()

        factory = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            join_transaction_mode="create_savepoint"
        )

        yield factory
        await transaction.rollback()


@pytest_asyncio.fixture
async def database_session(session_factory):
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def container(session_factory, test_settings):
    container = ApplicationContainer()
    container.configurations.configuration.from_pydantic(test_settings)

    container.gateways.session_factory.override(session_factory)
    yield container


@pytest_asyncio.fixture(scope="function")
async def client(container):
    app = create_fastapi_app()
    app.container = container
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def brand_repository(container):
    return await container.reference.brand_repository()


@pytest_asyncio.fixture
async def add_to_wishlist_usecase(container):
    return await container.wishlist.add_to_wishlist_usecase()