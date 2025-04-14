from abc import ABC, abstractmethod
from typing import List
from app.domain.pipelines.entities.jobs import Job

class IJobLoadToRepository(ABC):
    
    @abstractmethod
    async def insert(self, job:Job, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def insert_many(self, jobs: List[Job], *args, **kwargs):
        raise NotImplementedError