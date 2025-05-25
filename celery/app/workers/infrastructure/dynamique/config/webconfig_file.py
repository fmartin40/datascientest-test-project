import json
import os
from typing import List

from app.workers.entities.settings import WebsiteSettings
from app.workers.interfaces.iwebconfig import IWebsiteSettingsLoader

class WebsiteSettingsFileLoader(IWebsiteSettingsLoader):
    def __init__(self):
        self.folder_settings: str = "app/infrastructure/scrap/config/files"

    def load_website_settings(self, website: str) -> WebsiteSettings:
        try:
            with open(f'{self.folder_settings}/{website}.json', 'r') as f:
                return WebsiteSettings(**json.load(f))
        except Exception as exc:
            print(exc)
            raise 

    def list_available_websites(self) -> List[str]:
        return [f.replace('.json', '') for f in os.listdir(self.folder_settings) if f.endswith('.json')]
