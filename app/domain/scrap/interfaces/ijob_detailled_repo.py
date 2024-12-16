from abc import ABC, abstractmethod
from typing import List

from app.domain.scrap.entites.jobs import JobSummary

class IJobDetailledRepository(ABC):
    
    @abstractmethod
    async def create(self, job:JobSummary, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def create_many(self, jobs: List[JobSummary], *args, **kwargs):
        raise NotImplementedError