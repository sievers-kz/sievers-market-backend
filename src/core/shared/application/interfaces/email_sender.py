from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_id: str | None = None,
        template_data: dict | None = None,
    ):
        raise NotImplementedError
