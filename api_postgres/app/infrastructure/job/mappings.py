import logging
from typing import Dict, Optional
from app.domain.job.interfaces.imappings import IMappings
from app.infrastructure.models.models import (
    MappingTypeContratOrm,
    MappingModeTravailOrm,
    MappingDureeTravailOrm,
    MappingCompetenceOrm,
    TypeContratOrm,
    ModeTravailOrm,
    DureeTravailOrm,
    CompetenceOrm,
)

logger = logging.getLogger(__name__)

class Mappings(IMappings):
    async def list_type_contrat(self) -> dict:
        try:
            mapping_dict = {
                mapping.libelle: mapping.type_contrat.libelle if mapping.type_contrat else None
                for mapping in await MappingTypeContratOrm.all().prefetch_related("type_contrat")
            }
            for tc in await TypeContratOrm.all():
                if tc.libelle not in mapping_dict:
                    mapping_dict[tc.libelle] = tc.libelle
            return mapping_dict
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des types de contrat : {e}")
            return {}
    
    async def list_mode_travail(self) -> dict:
        try:
            mapping_dict = {
                mapping.libelle: mapping.mode_travail.libelle if mapping.mode_travail else None
                for mapping in await MappingModeTravailOrm.all().prefetch_related("mode_travail")
            }
            for mt in await ModeTravailOrm.all():
                if mt.libelle not in mapping_dict:
                    mapping_dict[mt.libelle] = mt.libelle
            return mapping_dict
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des modes de travail : {e}")
            return {}
    
    async def list_duree_travail(self) -> dict:
        try:
            mapping_dict = {
                mapping.libelle: mapping.duree_travail.libelle if mapping.duree_travail else None
                for mapping in await MappingDureeTravailOrm.all().prefetch_related("duree_travail")
            }
            for dt in await DureeTravailOrm.all():
                if dt.libelle not in mapping_dict:
                    mapping_dict[dt.libelle] = dt.libelle
            return mapping_dict
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des durées de travail : {e}")
            return {}
    
    async def list_competence(self) -> dict:
        try:
            mapping_dict = {
                mapping.libelle: mapping.competence.libelle if mapping.competence else None
                for mapping in await MappingCompetenceOrm.all().prefetch_related("competence")
            }
            for c in await CompetenceOrm.all():
                if c.libelle not in mapping_dict:
                    mapping_dict[c.libelle] = c.libelle
            return mapping_dict
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des compétences : {e}")
            return {}
