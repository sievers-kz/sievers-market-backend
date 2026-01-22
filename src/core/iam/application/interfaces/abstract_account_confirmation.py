from abc import ABC, abstractmethod


class AbstractAccountConfirmation(ABC):
    @abstractmethod
    async def send_confirmation_code(self, destination: str, code: str):
        raise NotImplementedError
