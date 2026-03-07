from abc import ABC, abstractmethod


class AbstractAccountNotifier(ABC):
    @abstractmethod
    async def send_confirmation_code(self, destination: str, code: str):
        raise NotImplementedError

    @abstractmethod
    async def send_password_recovery(self, destination: str, code: str):
        raise NotImplementedError
