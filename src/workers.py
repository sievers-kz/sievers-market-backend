from uuid import UUID

from arq import Retry
from arq.connections import RedisSettings
from loguru import logger

from src.configuration.dependencies.container import ApplicationContainer
from src.configuration.settings.settings import RedisConfig
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError


async def startup(ctx):
    container = ApplicationContainer()
    ctx["resend_sender"] = container.shared.resend_sender()
    ctx["verify_organization_registry_usecase"] = container.customer.verify_organization_registry_usecase()


async def send_otp_email(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код верификации Sievers",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для верификации аккаунта</h3>",  # noqa: E501
    )


async def send_otp_password_reset(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код для сброса пароля Sievers",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для сброса пароля</h3>",  # noqa: E501
    )


async def send_otp_change_email(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код подтверждения для изменения email",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для изменения email",
    )


async def send_otp_change_password(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код подтверждения для изменения пароля",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для изменения пароля</h3>",
    )


async def verify_organization_registry(ctx: dict, organization_id: str) -> None:
    usecase = await ctx["verify_organization_registry_usecase"]
    try:
        await usecase.execute(UUID(organization_id))
    except TaxpayerRegistryUnavailableError:
        job_try = ctx["job_try"]
        delay = min(60 * 2 ** (job_try - 1), 1800)
        logger.warning(
            "Taxpayer registry unavailable | organization_id={} try={} retry_in={}s",
            organization_id,
            job_try,
            delay,
        )
        raise Retry(defer=delay)


_redis_config = RedisConfig()


class WorkerSettings:
    functions = [
        send_otp_email,
        send_otp_password_reset,
        send_otp_change_email,
        send_otp_change_password,
        verify_organization_registry,
    ]

    on_startup = startup
    max_tries = 5

    redis_settings = RedisSettings(
        host=_redis_config.host,
        port=_redis_config.port,
        database=_redis_config.db,
        password=_redis_config.password,
    )
