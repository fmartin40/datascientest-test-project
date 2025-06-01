from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job


class IJobReader(ABC):

    @abstractmethod
    async def list(self, offset: int = 0, limit: int = 10) -> List[Job]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ids(self, ids: List[str]) -> List[Job]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, job_id: str) -> Optional[Job]:
        raise NotImplementedError

    @abstractmethod
    async def search_by_description(self, text: str) -> List[Job]:
        raise NotImplementedError
