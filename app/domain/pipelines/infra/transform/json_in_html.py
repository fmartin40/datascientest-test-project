import json
from typing import Dict, List
from bs4 import BeautifulSoup

from app.domain.pipelines.entities.jobs import Job
from app.domain.pipelines.entities.website import WebConfig
from app.domain.pipelines.interfaces.ijob_transform import IJobTransform


class TransformJsonInHtml(IJobTransform):

    async def transform(self, data: str, webconfig: WebConfig)->Job | List[Job]:
        soup = BeautifulSoup(data, "html.parser")
        
        #  Trouver la balise <script> avec l'id tag
        script_tag = soup.find(webconfig.tag)
        
        if script_tag:
            json_text = script_tag.string  # Récupérer le texte brut du script

            #  Charger le JSON en dictionnaire Python
            try:
                data = json.loads(json_text)
                print(" Données JSON extraites :", data)
                return data
            except json.JSONDecodeError as e:
                print(" Erreur lors du parsing JSON:", e)
        else:
            print(" Balise <script id='__NEXT_DATA__'> non trouvée")
