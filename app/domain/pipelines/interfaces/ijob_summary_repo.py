from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.jobs import JobSummary

class IJobSummaryRepository(ABC):
    
    @abstractmethod
    async def insert(self, job:JobSummary, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def insert_many(self, jobs: List[JobSummary], *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, job_id: int, *args, **kwargs):
        raise NotImplementedError