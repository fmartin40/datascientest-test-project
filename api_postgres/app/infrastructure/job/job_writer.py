from app.domain.job.entities.job_insert import JobCreate
from app.domain.job.interfaces.ijob_writer import IJobWriter  
from app.infrastructure.models.models import (
    EntrepriseOrm,
    DureeTravailOrm, CompetenceOrm, ModeTravailOrm, TypeContratOrm,
    SourceOrm, OffreEmploiOrm, VilleOrm
)
import logging
from tortoise.exceptions import IntegrityError

logger = logging.getLogger(__name__)

class JobWriter(IJobWriter):
    async def add(self, job: JobCreate) -> None:
        logger.error("Erreur d'intégrité lors de l'ajout de l'offre: ")
        try:
            # Vérifier si l'offre existe déjà
            existing_job = await OffreEmploiOrm.filter(job_id=job.job_id).first()
            if existing_job:
                logger.info(f"L'offre avec job_id {job.job_id} existe déjà. Opération ignorée.")
                return
                
            # Continuer avec l'insertion si l'offre n'existe pas
            entreprise_db = await self.add_entreprise(job.entreprise) # type: ignore
            ville_db = await self.add_ville(job.ville) # type: ignore
            source_db = await self.add_source(job.source) # type: ignore
            # duree_travail_db = await self.add_duree_travail(job.duree_travail)
            # mode_travail_db = await self.add_mode_travail(job.mode_travail)
            # type_contrat_db = await self.add_type_contrat(job.type_contrat)

            offre = await OffreEmploiOrm.create(
                job_id=job.job_id,
                date_creation=job.date_creation,
                libelle=job.libelle,
                source_id=source_db.id,
                
                entreprise=entreprise_db.id,
                ville=ville_db.id,
                type_contrat=job.type_contrat_id,
                duree_travail=job.duree_travail_id,
                mode_travail=job.mode_travail_id,
            )
            logger.info(f"Offre créée avec l'ID: {offre.id}")
            
            if job.competence_ids and len(job.competence_ids) > 0:
                # competences = []
                # for competence_libelle in job.competence:
                #     competence_obj = await self.add_competence(competence_libelle)
                #     competences.append(competence_obj)
                await offre.competences.add(*job.competence_ids)
                logger.info(f"Ajout de {len(job.competence_ids)} compétences pour l'offre {offre.id}")

        except IntegrityError as e:
            logger.error(f"Erreur d'intégrité lors de l'ajout de l'offre: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de l'offre: {str(e)}")
            raise

    async def delete(self, job_id: str) -> bool:
        try:
            deleted_count = await OffreEmploiOrm.filter(job_id=job_id).delete()
            return deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'offre {job_id}: {str(e)}")
            return False

    async def add_entreprise(self, entreprise: str) ->  EntrepriseOrm:
        try:
            obj, _ = await EntrepriseOrm.get_or_create(libelle=entreprise)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de l'entreprise {entreprise}: {str(e)}")
            raise
    
    async def add_ville(self, ville: str) -> VilleOrm:
        try:
            obj, _ = await VilleOrm.get_or_create(libelle=ville)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la ville {ville}: {str(e)}")
            raise


    async def add_duree_travail(self, duree_travail: str) -> DureeTravailOrm:
        try:
            obj, _ = await DureeTravailOrm.get_or_create(libelle=duree_travail)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la durée de travail {duree_travail}: {str(e)}")
            raise

    async def add_competence(self, competence: str) -> CompetenceOrm:
        try:
            obj, _ = await CompetenceOrm.get_or_create(libelle=competence)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la compétence {competence}: {str(e)}")
            raise

    async def add_mode_travail(self, mode_travail: str) -> ModeTravailOrm:
        try:
            obj, _ = await ModeTravailOrm.get_or_create(libelle=mode_travail)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du mode de travail {mode_travail}: {str(e)}")
            raise

    async def add_type_contrat(self, type_contrat: str) -> TypeContratOrm:
        try:
            obj, _ = await TypeContratOrm.get_or_create(libelle=type_contrat)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du type de contrat {type_contrat}: {str(e)}")
            raise

    async def add_source(self, source: str) -> SourceOrm:
        try:
            obj, _ = await SourceOrm.get_or_create(libelle=source)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la source {source}: {str(e)}")
            raise
