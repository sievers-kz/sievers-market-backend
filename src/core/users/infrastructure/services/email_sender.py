import asyncio
from abc import ABC, abstractmethod

from sendgrid import SendGridAPIClient, Mail


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

    async def send_email_confirmation(self, to_email: str, template_data: dict | None = None):
        message = Mail(from_email=self._from_email, to_emails=to_email)
        message.template_id = self._email_confirmation_template_id

        dynamic_data = {**(template_data or {})}
        message.dynamic_template_data = dynamic_data

        try:
            await asyncio.to_thread(self._client.send, message)
        except Exception as e:
            raise ValueError(f"Не удалось отправить письмо на почту: {to_email}. Ошибка: {e}")

    async def send_password_reset_confirmation(self, to_email: str, template_data: dict | None = None):
        message = Mail(from_email=self._from_email, to_emails=to_email)
        message.template_id = self._password_reset_template_id

        dynamic_data = {**(template_data or {})}
        message.dynamic_template_data = dynamic_data

        try:
            await asyncio.to_thread(self._client.send, message)
        except Exception as e:
            raise ValueError(f"Не удалось отправить письмо на почту: {to_email}. Ошибка: {e}")


class ConsoleEmailSender:
    async def send_confirmation_email(self, to: str, code: str):
        print("="*20, " MOCK EMAIL ", "="*20)
        print(f"TO: {to}")
        print(f"CODE: {code}")
        print("="*54)
