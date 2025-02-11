from abc import ABC, abstractmethod
from typing import List

from app.domain.pipelines.entities.website import WebConfig

class IWebconfig(ABC):
    
    @abstractmethod
    def get_website_config(name: str) -> WebConfig:
        raise NotImplementedError
    
    @abstractmethod
    def create_website_config(website: str) -> WebConfig:
        raise NotImplementedError