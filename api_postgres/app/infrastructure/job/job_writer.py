from app.domain.job.entities.job_insert import JobCreate
from app.domain.job.interfaces.ijob_writer import IJobWriter  
from app.infrastructure.models.models import (
    EntrepriseOrm,
    DureeTravailOrm, CompetenceOrm, ModeTravailOrm, TypeContratOrm,
    SourceOrm, OffreEmploiOrm, VilleOrm
)
import logging
from tortoise.exceptions import IntegrityError, DoesNotExist
from tortoise.models import Model

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
            type_contrat_db = await self.add_type_contrat(job.type_contrat_id) # type: ignore
            duree_travail_db = await self.add_duree_travail(job.duree_travail_id) # type: ignore
            mode_travail_db = await self.add_mode_travail(job.mode_travail_id) # type: ignore
            
            offre_data = {
                "job_id": job.job_id,
                "date_creation": job.date_creation,
                "libelle": job.libelle,
                "source_id": source_db.id,
                "entreprise_id": entreprise_db.id,
                "ville_id": ville_db.id,
                "type_contrat_id": type_contrat_db.id,
                "duree_travail_id": duree_travail_db.id,
                "mode_travail_id": mode_travail_db.id,
            }

            logger.info(f"Données à insérer dans OffreEmploi: {offre_data}")

            offre = await OffreEmploiOrm.create(
                job_id=job.job_id,
                date_creation=job.date_creation,
                libelle=job.libelle,
                source_id=source_db.id,
                url=job.url,
                entreprise_id=entreprise_db.id,
                ville_id=ville_db.id,
                type_contrat_id=type_contrat_db.id,
                duree_travail_id=duree_travail_db.id,
                mode_travail_id=mode_travail_db.id,
            )
            logger.info(f"Offre créée avec l'ID: {offre.id}")
            
            # if job.competence_ids and len(job.competence_ids) > 0:
            #     await offre.competences.add(*job.competence_ids)
            #     logger.info(f"Ajout de {len(job.competence_ids)} compétences pour l'offre {offre.id}")

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

    async def _add_relation_by_name(self, model: Model, libelle: str) -> Model:
        try:
            libelle = libelle.strip().lower()
            if not libelle:
                raise ValueError(f"Le libellé de {model.__name__} est vide.")
            try:
                obj, _ = await model.get_or_create(libelle=libelle)
            except IntegrityError:
                obj = await model.get(libelle=libelle)
            return obj
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la relation {model.__name__} {libelle}: {str(e)}")
            raise

    async def _add_relation_by_id(self, model: Model, id: int) -> Model:
        try:
            if not id:
                raise ValueError(f"L'ID de {model.__name__} est vide.")
            obj = await model.get(id=id)
            return obj
        except DoesNotExist:
            raise ValueError(f"Aucun {model.__name__} trouvé avec l'id {id}")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de {model.__name__} avec id {id}: {str(e)}")
            raise
    
    async def add_entreprise(self, entreprise: str) ->  EntrepriseOrm:
        try:
            return await self._add_relation_by_name(EntrepriseOrm, entreprise) # type: ignore

            # try:
            #     obj, _ = await EntrepriseOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await EntrepriseOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de l'entreprise {entreprise}: {str(e)}")
            raise
    
    async def add_ville(self, ville: str) -> VilleOrm:
        try:
            return await self._add_relation_by_name(VilleOrm, ville) # type: ignore

            # libelle = ville.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de ville est vide.")

            # try:
            #     obj, _ = await VilleOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await VilleOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la ville {ville}: {str(e)}")
            raise


    async def add_duree_travail(self, duree_travail_id: int) -> DureeTravailOrm:
        try:
            return await self._add_relation_by_id(DureeTravailOrm, duree_travail_id) # type: ignore

            # libelle = duree_travail.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de durée de travail est vide.")

            # try:
            #     obj, _ = await DureeTravailOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await DureeTravailOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la durée de travail {duree_travail_id  }: {str(e)}")
            raise

    async def add_competence(self, competence_id: int) -> CompetenceOrm:
        try:
            return await self._add_relation_by_id(CompetenceOrm, competence_id) # type: ignore
            # libelle = competence.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de compétence est vide.")

            # try:
            #     obj, _ = await CompetenceOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await CompetenceOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la compétence {competence_id}: {str(e)}")
            raise

    async def add_mode_travail(self, mode_travail_id: int) -> ModeTravailOrm:
        try:
            return await self._add_relation_by_id(ModeTravailOrm, mode_travail_id) # type: ignore
            # libelle = mode_travail.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de mode de travail est vide.")

            # try:
            #     obj, _ = await ModeTravailOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await ModeTravailOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du mode de travail {mode_travail_id}: {str(e)}")
            raise

    async def add_type_contrat(self, type_contrat_id: int) -> TypeContratOrm:
        try:
            return await self._add_relation_by_id(TypeContratOrm, type_contrat_id) # type: ignore
            # libelle = type_contrat.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de type de contrat est vide.")

            # try:
            #     obj, _ = await TypeContratOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await TypeContratOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du type de contrat {type_contrat_id}: {str(e)}")
            raise

    async def add_source(self, source: str) -> SourceOrm:
        try:
            return await self._add_relation_by_name(SourceOrm, source) # type: ignore
            # libelle = source.strip().lower()
            # if not libelle:
            #     raise ValueError("Le libellé de source est vide.")

            # try:
            #     obj, _ = await SourceOrm.get_or_create(libelle=libelle)
            # except IntegrityError:
            #     obj = await SourceOrm.get(libelle=libelle)

            # return obj
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la source {source}: {str(e)}")
            raise
