from abc import ABC, abstractmethod
from typing import List
from app.workers.entities.jobs import JobSummary, JobDetail

class IStaticExtractor(ABC):
    @abstractmethod
    async def extract_summaries(self, *args, **kwargs) -> List[JobSummary]:
        raise NotImplementedError
    
    @abstractmethod
    async def extract_details(self, *args, **kwargs) -> JobDetail | None:
        raise NotImplementedError
    
    