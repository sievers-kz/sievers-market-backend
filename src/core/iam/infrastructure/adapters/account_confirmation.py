from src.core.iam.application.interfaces.abstract_account_notifier import AbstractAccountNotifier
from src.core.shared.infrastructure.services.email_sender import AbstractEmailSender


class EmailNotifierAdapter(AbstractAccountNotifier):
    def __init__(
        self,
        sender: AbstractEmailSender,
        email_confirmation_template: str,
        password_recovery_template: str
    ):
        self._sender = sender
        self._email_confirmation_template = email_confirmation_template
        self._password_recovery_template = password_recovery_template

    async def send_confirmation_code(self, destination: str, code: str):
        await self._sender.send_email(
            to_email=destination,
            template_id=self._email_confirmation_template,
            template_data={"code": code, "message": "Ваш код подтверждения почты"}
        )

    async def send_password_recovery(self, destination: str, code: str):
        await self._sender.send_email(
            to_email=destination,
            template_id=self._password_recovery_template,
            template_data={"code": code, "message": "Ваш код для обновления пароля"}
        )

