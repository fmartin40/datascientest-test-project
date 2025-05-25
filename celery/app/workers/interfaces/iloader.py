from abc import ABC, abstractmethod
from typing import List
from app.workers.entities.jobs import JobDetail

class ILoader(ABC):
    
    @abstractmethod
    async def insert(self, job:JobDetail, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def insert_many(self, jobs: List[JobDetail], *args, **kwargs):
        raise NotImplementedError
    
    