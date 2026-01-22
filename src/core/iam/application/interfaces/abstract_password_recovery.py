from abc import ABC, abstractmethod


class AbstractPasswordRecovery(ABC):
    @abstractmethod
    async def send_password_recovery(self, destination: str, code: str):
        raise NotImplementedError
