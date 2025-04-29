from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.job.entities.jobs import Job

class IJobRepository(ABC):
    @abstractmethod
    def add(self, job: Job) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Job]:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: str) -> bool:
        pass 