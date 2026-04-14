from dependency_injector import containers, providers

from src.configuration.dependencies.customer import CustomerContainer
from src.configuration.dependencies.configuration import ConfigurationContainer
from src.configuration.dependencies.gateways import GatewaysContainer
from src.configuration.dependencies.iam import IAMContainer
from src.configuration.dependencies.machinery import MachineryContainer
from src.configuration.dependencies.media import MediaContainer
from src.configuration.dependencies.reference import ReferenceContainer
from src.configuration.dependencies.shared import SharedContainer
from src.configuration.dependencies.wishlist import WishlistContainer


class ApplicationContainer(containers.DeclarativeContainer):
    configurations = providers.Container(
        ConfigurationContainer
    )

    gateways = providers.Container(
        GatewaysContainer,
        database_config=configurations.database,
        sendgrid_config=configurations.sendgrid,
        redis_config=configurations.redis,
    )

    shared = providers.Container(
        SharedContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session,
        redis_client=gateways.redis_client,
        arq_pool=gateways.arq_pool,
        resend_config=configurations.resend_config,
    )

    reference = providers.Container(
        ReferenceContainer,
        database_session=gateways.database_session
    )

    wishlist = providers.Container(
        WishlistContainer,
        database_session=gateways.database_session
    )

    machinery = providers.Container(
        MachineryContainer,
        database_session=gateways.database_session,
        attribute_service=reference.attribute_service,
        wishlist_service=wishlist.wishlist_service,
        brand_repository=reference.brand_repository,
    )

    media = providers.Container(
        MediaContainer,
        object_storage_config=configurations.object_storage,
        database_session=gateways.database_session
    )

    customer = providers.Container(
        CustomerContainer,
        database_session=gateways.database_session,
        session_factory=gateways.session_factory,
    )

    iam = providers.Container(
        IAMContainer,
        auth_config=configurations.authentication,
        database_session=gateways.database_session,
        customer_service=customer.customer_service,
        console_email_sender=shared.console_email_sender,
        redis_service=shared.redis_service,
        arq_service=shared.arq_service,
    )
