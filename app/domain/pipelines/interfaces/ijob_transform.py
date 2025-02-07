from abc import ABC, abstractmethod
from typing import Dict, List

from app.domain.pipelines.entities.jobs import Job
from app.domain.pipelines.entities.website import WebConfig

class IJobTransform(ABC):
    
    @abstractmethod
    async def transform(self, data: str | Dict, webconfig: WebConfig, *args, **kwargs)->Job | List[Job]:
        raise NotImplementedError
    
   