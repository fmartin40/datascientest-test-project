from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job

class IJobWriter(ABC):
    @abstractmethod
    async def add(self, job: Job) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, job: Job) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, job_id: str) -> bool:
        raise NotImplementedError