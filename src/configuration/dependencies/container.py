from dependency_injector import containers, providers

from src.configuration.dependencies.buyer import BuyerContainer
from src.configuration.dependencies.configuration import ConfigurationContainer
from src.configuration.dependencies.gateways import GatewaysContainer
from src.configuration.dependencies.iam import IAMContainer
from src.configuration.dependencies.machinery import MachineryContainer
from src.configuration.dependencies.reference import ReferenceContainer
from src.configuration.dependencies.seller import SellerContainer
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
    )

    shared = providers.Container(
        SharedContainer,
        session_factory=gateways.session_factory,
        database_session=gateways.database_session
    )

    reference = providers.Container(
        ReferenceContainer,
        database_session=gateways.database_session
    )

    buyer = providers.Container(
        BuyerContainer,
        database_session=gateways.database_session,
        session_factory=gateways.session_factory,
    )

    seller = providers.Container(
        SellerContainer,
        database_session=gateways.database_session,
        session_factory=gateways.session_factory,
    )

    machinery = providers.Container(
        MachineryContainer,
        database_session=gateways.database_session,
        attribute_service=reference.attribute_service
    )

    wishlist = providers.Container(
        WishlistContainer,
        database_session=gateways.database_session
    )

    iam = providers.Container(
        IAMContainer,
        auth_config=configurations.authentication,
        database_session=gateways.database_session,
        buyer_service=buyer.buyer_service,
        seller_service=seller.seller_service,
        console_email_sender=shared.console_email_sender,
        email_confirmation_template=configurations.sendgrid.email_confirmation_template_id,
        password_recovery_template=configurations.sendgrid.password_recovery_template_id
    )
