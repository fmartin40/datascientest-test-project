from abc import ABC, abstractmethod
from typing import Dict, List

from app.domain.pipelines.entities.jobs import Job, JobDetail, JobSummary
from app.domain.pipelines.entities.website import WebConfig

class IJobTransform(ABC):
    
    @abstractmethod
    async def transform_to_job_summaries(self, data: str, webconfig: WebConfig)->List[JobSummary]:
        raise NotImplementedError
    
    @abstractmethod
    async def transform_to_job_detail(self, data: str, webconfig: WebConfig)->JobDetail | List[JobDetail]:
        raise NotImplementedError
    