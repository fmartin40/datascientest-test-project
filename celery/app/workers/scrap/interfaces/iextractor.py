from abc import ABC, abstractmethod
from typing import List
from app.workers.scrap.entities.jobs import JobSummary, JobDetail

class IExtractor(ABC):
    @abstractmethod
    async def extract(self, *args, **kwargs) -> List[JobSummary]|JobDetail:
        raise NotImplementedError
    
    