from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.jobs import JobDetail, JobSummary

class IJobScraper(ABC):
    
    @abstractmethod
    async def scrap_jobs_summaries(self, query: str, *args, **kwargs)->List[JobSummary]:
        raise NotImplementedError
    
    @abstractmethod
    async def scrap_job_detail(self, url: str, website: str, *args, **kwargs)->JobDetail:
        raise NotImplementedError