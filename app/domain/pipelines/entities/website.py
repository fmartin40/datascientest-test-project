
from dataclasses import dataclass
from typing import Dict


## objet vraiment temporaire, l'idee sci est de trouver une espece de config qui est renvoyé pour chaque site
# cette config contiendrait l'url pour faire une recherche, l'url du detail d'une offre*
# les differentes parametres propres a ce site pour scraper etc
# a developper

@dataclass
class WebConfig:
    name: str
    url_summaries: str
    url_detail: str 
    tag: Dict | str