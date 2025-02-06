from abc import ABC, abstractmethod
from typing import Dict, List

from app.domain.pipelines.entities.jobs import Job

class IJobTransform(ABC):
    
    @abstractmethod
    async def transform(self, data: str | Dict, *args, **kwargs)->Job | List[Job]:
        raise NotImplementedError
    
   