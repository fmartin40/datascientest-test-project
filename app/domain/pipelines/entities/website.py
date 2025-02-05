
from typing import Dict
from app.domain.common.interface.entity import Entity

class WebConfig(Entity):
    name: str
    url: str
    tag: Dict | str