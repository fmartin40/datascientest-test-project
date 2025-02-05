from abc import ABC, abstractmethod
from typing import List
from app.domain.pipelines.entities.jobs import JobDetail

class IJobDetailledRepository(ABC):
    
    @abstractmethod
    async def insert(self, job:JobDetail, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def insert_many(self, jobs: List[JobDetail], *args, **kwargs):
        raise NotImplementedError