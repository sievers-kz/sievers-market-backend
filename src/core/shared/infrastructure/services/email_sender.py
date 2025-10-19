import asyncio
from abc import ABC, abstractmethod

from python_http_client import UnauthorizedError, ForbiddenError, BadRequestsError
from sendgrid import SendGridAPIClient, Mail

from src.core.shared.infrastructure.exceptions.exception_classes import EmailSenderError, EmailSenderConfigurationError, \
    EmailSenderRequestsError


class AbstractEmailSender(ABC):
    @abstractmethod
    async def send_email_confirmation(self, to_email: str, template_data: dict | None = None):
        raise NotImplementedError

    @abstractmethod
    async def send_password_reset_confirmation(self, to_email: str, template_data: dict | None = None):
        raise NotImplementedError


class SendGridEmailSender(AbstractEmailSender):
    def __init__(
        self, api_key: str,
        from_email: str,
        email_confirmation_template_id: str,
        password_reset_template_id: str
    ):
        self._api_key = api_key
        self._from_email = from_email
        self._client = SendGridAPIClient(self._api_key)
        self._email_confirmation_template_id = email_confirmation_template_id
        self._password_reset_template_id = password_reset_template_id

    async def _send_email_confirmation(self, to_email: str, template_id: str, template_data: dict | None = None):
        message = Mail(from_email=self._from_email, to_emails=to_email)
        message.template_id = template_id
        message.dynamic_template_data = template_data or {}

        try:
            await asyncio.to_thread(self._client.send, message)

        except (UnauthorizedError, ForbiddenError) as exc:
            raise EmailSenderConfigurationError(
                code="email_sender_configuration_error",
                details=str(exc)
            ) from exc

        except BadRequestsError as exc:
            raise EmailSenderRequestsError(
                code="email_sender_requests_error",
                details=str(exc),
                context={
                    "to_email": to_email,
                    "template_id": template_id,
                    "template_data": template_data
                }
            ) from exc

        except Exception as exc:
            raise EmailSenderError(
                code="unexpected_error",
                details=str(exc)
            ) from exc

    async def send_email_confirmation(self, to_email: str, template_data: dict | None = None):
        await self._send_email_confirmation(to_email, self._email_confirmation_template_id, template_data)

    async def send_password_reset_confirmation(self, to_email: str, template_data: dict | None = None):
        await self._send_email_confirmation(to_email, self._password_reset_template_id, template_data)


class ConsoleEmailSender:
    async def send_email_confirmation(self, to_email: str, template_data: dict | None = None):
        print("="*24, "EMAIL VERIFICATION MESSAGE", "="*24)
        print(f"FROM: noreply@agrow.asia")
        print(f"TO: {to_email}")
        print(f"SUBJECT: Hello! Confirm your email. Just copy and paste this token:")
        print(f"TOKEN: {template_data.get('confirmation_token')}")
        print("="*32, ""*32)

    async def send_password_reset_confirmation(self, to_email: str, template_data: dict | None = None):
        print("="*24, "PASSWORD RESET CONFIRMATION", "="*24)
        print(f"FROM: noreply@agrow.asia")
        print(f"TO: {to_email}")
        print(f"SUBJECT: Hello! Let's to reset your password. Just use this token:")
        print(f"TOKEN: {template_data.get('reset_password_token')}")
        print("="*32, ""*32)
