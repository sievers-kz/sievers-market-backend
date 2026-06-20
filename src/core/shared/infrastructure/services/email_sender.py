import asyncio

import resend
from sendgrid import Content, Mail, SendGridAPIClient

from src.core.shared.application.interfaces.email_sender import IEmailSender


class SendGridEmailSender(IEmailSender):
    def __init__(
        self,
        api_key: str,
        from_email: str,
    ):
        self._client = SendGridAPIClient(api_key)
        self._from_email = from_email

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_id: str | None = None,
        template_data: dict | None = None,
        html_content: str | None = None,
    ):
        message = Mail(from_email=self._from_email, to_emails=to_email, subject=subject)

        if template_id:
            message.template_id = template_id
            message.dynamic_template_data = template_data or {}
        else:
            message.content = Content("text/html", html_content)

        await asyncio.to_thread(self._client.send, message)


class ConsoleEmailSender(IEmailSender):
    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_id: str | None = None,
        template_data: dict | None = None,
        html_content: str | None = None,
    ) -> None:
        print("\n" + "=" * 50)
        print("[MOCK EMAIL] From: development@agrow.asia")
        print(f"[MOCK SUBJECT] Subject: {subject}")
        print(f"[MOCK EMAIL] To: {to_email}")

        if template_id:
            print(f"[MOCK EMAIL] Tpl: {template_id}")
        else:
            print(f"[MOCK HTML] Html: {html_content}")

        print(f"[MOCK EMAIL] Data: {template_data or {}}")
        print("=" * 50 + "\n")


class ResendEmailSender(IEmailSender):
    def __init__(self, api_key: str, from_email: str):
        resend.api_key = api_key
        self._from_email = from_email

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_id: str | None = None,
        template_data: dict | None = None,
        html_content: str | None = None,
    ) -> None:
        if not template_id and not html_content:
            raise ValueError("Письмо должно содержать либо шаблон, либо HTML")

        params = {
            "from": self._from_email,
            "to": [to_email],
            "subject": subject,
        }

        if template_id:
            params["template"] = {
                "id": template_id,
                "variables": template_data or {},
            }
        else:
            params["html"] = html_content

        await resend.Emails.send_async(params)
