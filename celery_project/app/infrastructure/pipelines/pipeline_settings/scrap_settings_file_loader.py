import json
from typing import Dict

from app.workers.pipelines.entities.settings import WebsiteSettings
from app.workers.pipelines.interfaces.iwebsite_settings import IWebsiteSettingsLoader
from app.core.config import settings

class WebsiteSettingsFileLoader(IWebsiteSettingsLoader):
    
    def load_website_settings(self, website: str) -> WebsiteSettings:
        try:
            with open(f'{settings.CONFIG_FOLDER}/{website}.json', 'r') as f:
                return WebsiteSettings(**json.load(f))
        except Exception as exc:
            print(exc)
            raise 

    def create_website_settings(self, extract_service: Dict) -> WebsiteSettings:
        raise NotImplementedError
    