from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job

class IJobReader(ABC):
    
    @abstractmethod
    async def list(self) -> List[Job]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, job_id: str) -> Optional[Job]:
        raise NotImplementedError

    