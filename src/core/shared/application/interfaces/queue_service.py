from abc import ABC, abstractmethod


class IQueueService(ABC):
    @abstractmethod
    async def enqueue(self, task_name: str, **kwargs) -> None:
        raise NotImplementedError
