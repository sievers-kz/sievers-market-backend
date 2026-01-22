import asyncio
from abc import ABC, abstractmethod

from sendgrid import SendGridAPIClient, Mail


class AbstractEmailSender(ABC):
    @abstractmethod
    async def send_email(self, to_email: str, template_id: str, template_data: dict | None = None):
        raise NotImplementedError


class SendGridEmailSender(AbstractEmailSender):
    def __init__(
        self,
        api_key: str,
        from_email: str,
    ):
        self._client = SendGridAPIClient(api_key)
        self._from_email = from_email

    async def send_email(self, to_email: str, template_id: str, template_data: dict | None = None):
        message = Mail(from_email=self._from_email, to_emails=to_email)
        message.template_id = template_id
        message.dynamic_template_data = template_data or {}
        await asyncio.to_thread(self._client.send, message)


class ConsoleEmailSender(AbstractEmailSender):
    async def send_email(self, to_email: str, template_id: str, template_data: dict | None = None) -> None:
        print("\n" + "="*50)
        print(f"[MOCK EMAIL] From: SYSTEM")
        print(f"[MOCK EMAIL] To:   {to_email}")
        print(f"[MOCK EMAIL] Tpl:  {template_id}")
        print(f"[MOCK EMAIL] Data: {template_data}")
        print("="*50 + "\n")
