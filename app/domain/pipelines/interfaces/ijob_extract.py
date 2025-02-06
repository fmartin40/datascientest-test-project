from abc import ABC, abstractmethod
from typing import List

class IJobExtract(ABC):
    
    @abstractmethod
    async def extract_jobs_summaries(self, query: str, *args, **kwargs)->List[str]:
        raise NotImplementedError
    
    @abstractmethod
    async def extract_job_detail(self, url: str, *args, **kwargs)->str:
        raise NotImplementedError