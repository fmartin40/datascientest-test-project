from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.webconfig import WebConfig

class IWebconfig(ABC):
    
    @abstractmethod
    def get_website_config(self, website: str) -> WebConfig:
        raise NotImplementedError
    
    @abstractmethod
    def create_website_config(self, website: WebConfig) -> WebConfig:
        raise NotImplementedError