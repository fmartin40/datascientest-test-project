from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class IJobRepo(ABC):
    @abstractmethod
    async def get_job_detail(self, task_id: str) -> Optional[Dict]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_job_summaries(self, task_id: str) -> Optional[List[Dict]]:
        raise NotImplementedError 