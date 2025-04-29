from abc import ABC, abstractmethod

from app.workers.common.entities.jobs import JobDetail

class ITransformer(ABC):
    @abstractmethod
    async def transform(self, jobdetail: JobDetail, *args, **kwargs):
        raise NotImplementedError
    
    