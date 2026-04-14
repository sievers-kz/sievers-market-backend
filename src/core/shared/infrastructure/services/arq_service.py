from arq import ArqRedis

from src.core.shared.application.interfaces.queue_service import IQueueService


class ArqService(IQueueService):
    def __init__(self, pool: ArqRedis):
        self.pool = pool

    async def enqueue(self, task_name: str, **kwargs) -> None:
        await self.pool.enqueue_job(task_name, **kwargs)
