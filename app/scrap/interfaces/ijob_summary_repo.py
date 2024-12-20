from abc import ABC, abstractmethod
from typing import List

from app.scrap.entites.jobs import JobSummary

class IJobSummaryRepository(ABC):
    
    @abstractmethod
    async def create(self, job:JobSummary, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def create_many(self, jobs: List[JobSummary], *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, job_id: int, *args, **kwargs):
        raise NotImplementedError