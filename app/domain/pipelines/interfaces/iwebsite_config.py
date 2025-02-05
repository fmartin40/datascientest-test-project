from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.jobs import JobDetail, JobSummary


class IWebsiteConfig(ABC):
    """ 
        Interface pour remonter les configurations de scrap des site web
    """
    
    @abstractmethod
    async def get_website_config(self, website: str, **kwargs)->List[JobSummary]:
        raise NotImplementedError
    
    