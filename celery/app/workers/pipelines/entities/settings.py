
from typing import Dict, List
from pydantic import BaseModel


class WebsiteInfo(BaseModel):
    website: str
    root_url: str
    request_url: str
    query_space_replacement: str


class ParserSettings(BaseModel):
    role: str
    step: str
    format: str
    actif: bool
    selectors: Dict
    pagination: str | None = None
    json_tag: Dict | None = None
    json_required_keys: List[str] | None = None


class WebsiteSettings(BaseModel):
    website_info: WebsiteInfo
    parsers: List[ParserSettings]
    





    
    