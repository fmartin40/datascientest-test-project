from abc import ABC, abstractmethod
from typing import List

from app.domain.scrap.entites.jobs import JobDetailled, JobSummary

class IScrapeJob(ABC):
    
    @abstractmethod
    async def scrap_jobs_summaries(self, query: str, website: str, *args, **kawargs)->List[JobSummary]:
        raise NotImplementedError
    
    @abstractmethod
    async def scrap_job_content(self, url: str, website: str, *args, **kawargs)->List[JobDetailled]:
        raise NotImplementedError