from app.domain.job.entities.job_insert import JobCreate
from app.domain.job.interfaces.ijob_writer import IJobWriter  
from app.infrastructure.models.models import (
    EntrepriseOrm, SalaireOrm, FormationOrm, LangueOrm, ExperienceOrm,
    DureeTravailOrm, CompetenceOrm, ModeTravailOrm, TypeContratOrm,
    SourceOrm, OffreEmploiOrm, VilleOrm
)
import logging
from tortoise.exceptions import IntegrityError

logger = logging.getLogger(__name__)

class JobWriter(IJobWriter):
    async def add(self, job: JobCreate) -> None:
        try:
            # Vérifier si l'offre existe déjà
            existing_job = await OffreEmploiOrm.filter(job_id=job.job_id).first()
            if existing_job:
                logger.info(f"L'offre avec job_id {job.job_id} existe déjà. Opération ignorée.")
                return
                
            # Continuer avec l'insertion si l'offre n'existe pas
            entreprise_db = await self.add_entreprise(job.entreprise)
            ville_db = await self.add_ville(job.ville)
            salaire_db = await self.add_salaire(str(job.salaire) if job.salaire is not None else "")
            experience_db = await self.add_experience(job.experience)
            duree_travail_db = await self.add_duree_travail(job.duree_travail)
            mode_travail_db = await self.add_mode_travail(str(job.mode_travail_id))
            type_contrat_db = await self.add_type_contrat(job.type_contrat)
            
            offre = await OffreEmploiOrm.create(
                job_id=job.job_id,
                date_creation=job.date_creation,
                source_id=job.source_id,
                libelle=job.libelle,
                entreprise=entreprise_db,
                ville=ville_db,
                salaire=salaire_db,
                experience=experience_db,
                duree_travail=duree_travail_db,
                mode_travail=mode_travail_db,
                type_contrat=type_contrat_db,
            )
            logger.info(f"Offre créée avec l'ID: {offre.id}")
            
            # Gestion des relations many-to-many
            if job.formation and len(job.formation) > 0:
                formations = []
                for formation_libelle in job.formation:
                    formation_obj = await self.add_formation(formation_libelle)
                    formations.append(formation_obj)
                await offre.formations.add(*formations)
                logger.info(f"Ajout de {len(formations)} formations pour l'offre {offre.id}")
            
            if job.langue and len(job.langue) > 0:
                langues = []
                for langue_libelle in job.langue:
                    langue_obj = await self.add_langue(langue_libelle)
                    langues.append(langue_obj)
                await offre.langues.add(*langues)
                logger.info(f"Ajout de {len(langues)} langues pour l'offre {offre.id}")
            
            if job.competence and len(job.competence) > 0:
                competences = []
                for competence_libelle in job.competence:
                    competence_obj = await self.add_competence(competence_libelle)
                    competences.append(competence_obj)
                await offre.competences.add(*competences)
                logger.info(f"Ajout de {len(competences)} compétences pour l'offre {offre.id}")

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

    async def add_salaire(self, salaire: str) -> SalaireOrm:
        try:
            obj, _ = await SalaireOrm.get_or_create(libelle=salaire)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du salaire {salaire}: {str(e)}")
            raise

    async def add_formation(self, formation: str) -> FormationOrm:
        try:
            obj, _ = await FormationOrm.get_or_create(libelle=formation)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la formation {formation}: {str(e)}")
            raise

    async def add_langue(self, langue: str) -> LangueOrm:
        try:
            obj, _ = await LangueOrm.get_or_create(libelle=langue)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la langue {langue}: {str(e)}")
            raise

    async def add_experience(self, experience: str) -> ExperienceOrm:
        try:
            obj, _ = await ExperienceOrm.get_or_create(libelle=experience)
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de l'expérience {experience}: {str(e)}")
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
