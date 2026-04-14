from arq.connections import RedisSettings

from src.configuration.dependencies.container import ApplicationContainer


async def startup(ctx):
    container = ApplicationContainer()
    ctx["resend_sender"] = container.shared.resend_sender()


async def send_otp_email(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject=f"Ваш код верификации AGROW",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для верификации аккаунта</h3>",
    )


async def send_otp_password_reset(ctx, to: str, code: str):
    sender = ctx["resend_sender"]
    await sender.send_email(
        to_email=to,
        subject="Ваш код для сброса пароля AGROW",
        html_content=f"<h3>Ваш код <strong>{code}</strong> для сброса пароля</h3>",
    )


class WorkerSettings:
    functions = [send_otp_email, send_otp_password_reset]
    on_startup = startup
    max_retries = 5
    redis_settings = RedisSettings(host="localhost", port=6379)
