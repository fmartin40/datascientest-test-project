from abc import ABC, abstractmethod
from typing import Dict, List

from app.domain.pipelines.entities.jobs import Job, JobDetail, JobSummary
from app.domain.pipelines.entities.extractconfig import ExtractConfig

class IJobTransform(ABC):
    
    @abstractmethod
    async def transform_to_job_summaries(self, data: str, extract_config: ExtractConfig)->List[JobSummary]:
        raise NotImplementedError
    
    @abstractmethod
    async def transform_to_job_detail(self, data: str, extract_config: ExtractConfig)->JobDetail | List[JobDetail]:
        raise NotImplementedError
    