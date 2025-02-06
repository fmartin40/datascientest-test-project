
from typing import Dict

from app.domain.pipelines.entities.website import WebConfig, Website
from app.domain.pipelines.interfaces.iwebsite_config import IWebsiteConfig

class FakeWebConfig(IWebsiteConfig):
    """
        Classe qui simue l'interrogation d'une base de donnée pour remonter les configuration de scrap en fonction du site

    """
    def get_website_config(self, website: str) -> WebConfig:
        match website:
            case 'emplois-informatique':
                return WebConfig(
                    name="emplois-informatique",
                    url_summaries="",
                    url_detail="https://www.emplois-informatique.fr/cdi/technical-data-engineer-senior-h-f-6832572",
                    tag={"type": "application/ld+json"}
                )
            case 'glassdoor':
                return WebConfig(
                    name="glassdoor",
                    url_summaries="",
                    url_detail="https://www.glassdoor.fr/Emploi/paris-75-france-data-engineer-emplois-SRCH_IL.0,15_IC2881970_KO16,29.htm",
                    tag={"id": "__NEXT_DATA__"}
                )
            case 'jobintree':
                return WebConfig(
                    name="jobintree",
                    url_summaries="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}",
                    url_detail="https://www.jobintree.com/emplois/60831578.html",
                    tag={"type": "application/ld+json"}
                )
            case 'muse':
                return WebConfig(
                    name="muse",
                    url_summaries="",
                    url_detail="https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833",
                    tag={"id": "__NEXT_DATA__"}
                )
            case 'optioncarriere':
                return WebConfig(
                    name="option_carriere",
                    url_summaries="",
                    url_detail="https://www.optioncarriere.com/jobad/fraf74734f528917804df9de514029dbb4",
                    tag={"type": "application/ld+json"}
                )
            case _:
                raise ValueError(f"Configuration inconnue pour le site : {website}")



        

        

       