from dependency_injector import containers, providers

from src.configuration.dependencies.admin import AdminContainer
from src.configuration.dependencies.catalog import CatalogContainer
from src.configuration.dependencies.configuration import ConfigurationContainer
from src.configuration.dependencies.customer import CustomerContainer
from src.configuration.dependencies.gateways import GatewaysContainer
from src.configuration.dependencies.iam import IAMContainer
from src.configuration.dependencies.listing import ListingContainer
from src.configuration.dependencies.media import MediaContainer
from src.configuration.dependencies.reference import ReferenceContainer
from src.configuration.dependencies.shared import SharedContainer


class ApplicationContainer(containers.DeclarativeContainer):
    configurations = providers.Container(ConfigurationContainer)

    gateways = providers.Container(
        GatewaysContainer,
        database_config=configurations.database,
        redis_config=configurations.redis,
        minio_config=configurations.minio_config,
        sentry_config=configurations.sentry_config,
        meilisearch_config=configurations.meilisearch_config,
    )

    catalog = providers.Container(
        CatalogContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
    )

    shared = providers.Container(
        SharedContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        redis_client=gateways.redis_client,
        arq_pool=gateways.arq_pool,
        resend_config=configurations.resend_config,
        app_config=configurations.configuration,
        meilisearch_client=gateways.meilisearch_client,
    )

    reference = providers.Container(
        ReferenceContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
    )

    customer = providers.Container(
        CustomerContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        redis_service=shared.redis_service,
        taxpayer_registry_config=configurations.taxpayer_registry_config,
        arq_service=shared.arq_service,
    )

    iam = providers.Container(
        IAMContainer,
        auth_config=configurations.authentication,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        console_email_sender=shared.console_email_sender,
        redis_service=shared.redis_service,
        arq_service=shared.arq_service,
        bloom_filter=gateways.bloom_filter,
    )

    listing = providers.Container(
        ListingContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        attribute_validation=catalog.attribute_validation,
        meilisearch_service=shared.meilisearch_service,
        organization_service=customer.organization_service,
    )

    media = providers.Container(
        MediaContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        minio_client=gateways.minio_client,
        minio_public_client=gateways.minio_public_client,
        minio_config=configurations.minio_config,
    )

    admin = providers.Container(
        AdminContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        account_repository=iam.account_repository,
    )
