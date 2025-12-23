from dependency_injector import containers, providers

from src.configuration.dependencies.configuration import ConfigurationContainer
from src.configuration.dependencies.gateways import GatewaysContainer
from src.configuration.dependencies.iam import IAMContainer
from src.configuration.dependencies.listings import ListingContainer
from src.configuration.dependencies.references import ReferenceContainer


class ApplicationContainer(containers.DeclarativeContainer):
    configurations = providers.Container(ConfigurationContainer)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.auth.auth_routers",
            "src.api.users.user_routers",
            "src.api.listings.routers",
            "src.api.references.routers",
        ]
    )

    gateways = providers.Container(
        GatewaysContainer,
        database_config=configurations.database,
        sendgrid_config=configurations.sendgrid
    )

    iam = providers.Container(
        IAMContainer,
        auth_config=configurations.authentication,
        session_factory=gateways.session_factory,
        sendgrid_sender=gateways.sendgrid_sender
    )

    listing = providers.Container(
        ListingContainer,
        session_factory=gateways.session_factory
    )

    reference = providers.Container(
        ReferenceContainer,
        session_factory=gateways.session_factory
    )