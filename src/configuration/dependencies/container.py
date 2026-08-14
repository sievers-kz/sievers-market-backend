from dependency_injector import containers, providers

from src.configuration.dependencies.catalog import CatalogContainer
from src.configuration.dependencies.configuration import ConfigurationContainer
from src.configuration.dependencies.customer import CustomerContainer
from src.configuration.dependencies.gateways import GatewaysContainer
from src.configuration.dependencies.iam import IAMContainer
from src.configuration.dependencies.listing import ListingContainer
from src.configuration.dependencies.media import MediaContainer
from src.configuration.dependencies.reference import ReferenceContainer
from src.configuration.dependencies.shared import SharedContainer
from src.configuration.dependencies.vendor import VendorContainer


class ApplicationContainer(containers.DeclarativeContainer):
    configurations = providers.Container(ConfigurationContainer)

    gateways = providers.Container(
        GatewaysContainer,
        database_config=configurations.database,
        sendgrid_config=configurations.sendgrid,
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
    )

    media = providers.Container(
        MediaContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        minio_client=gateways.minio_client,
        minio_config=configurations.minio_config,
    )

    vendor = providers.Container(
        VendorContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        phone_normalizer=shared.phone_normalizer,
        customer_service=customer.customer_service,
        redis_service=shared.redis_service,
        kgd_settings=configurations.kgd_settings,
    )
