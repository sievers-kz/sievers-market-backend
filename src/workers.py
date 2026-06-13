from arq.connections import RedisSettings

from src.configuration.dependencies.container import ApplicationContainer
from src.configuration.settings.settings import RedisConfig


async def startup(ctx):
    container = ApplicationContainer()
    ctx["resend_sender"] = container.shared.resend_sender()


async def send_otp_email(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код верификации AGROW",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для верификации аккаунта</h3>",  # noqa: E501
    )


async def send_otp_password_reset(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код для сброса пароля AGROW",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для сброса пароля</h3>",  # noqa: E501
    )


async def send_otp_change_email(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код подтверждения для изменения email",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для изменения email",
    )


async def send_otp_change_phone(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код подтверждения для изменения номера телефона",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для изменения номера телефона",  # noqa: E501
    )


_redis_config = RedisConfig()


class WorkerSettings:
    functions = [
        send_otp_email,
        send_otp_password_reset,
        send_otp_change_email,
        send_otp_change_phone,
    ]

    on_startup = startup
    max_retries = 5

    redis_settings = RedisSettings(
        host=_redis_config.host,
        port=_redis_config.port,
        database=_redis_config.db,
        password=_redis_config.password,
    )
