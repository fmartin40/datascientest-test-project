from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide
from app.core.container import ContainerService
from app.domain.job.entities.job_insert import (
    JobCreate,
    # EntrepriseCreate, LangueCreate, DureeTravailCreate,
    # CompetenceCreate, ModeTravailCreate, TypeContratCreate, SourceCreate
)
from app.infrastructure.job.job_writer import JobWriter
from tortoise.exceptions import IntegrityError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["write job infos"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
@inject
async def create_job(
    payload: JobCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer]),
):
    try:
        logger.error(f"offre a creer: {payload.model_dump()}")
        await job_writer.add(payload)
        return {"status": "success", "message": "Offre d'emploi créée avec succès"}
    except IntegrityError as e:
        logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
        if "duplicate key value violates unique constraint" in str(e):
            return {
                "status": "success",
                "message": "L'offre existe déjà, aucune modification apportée",
            }
        return {
            "status": "warning",
            "message": f"Problème d'intégrité des données: {str(e)}",
            "error": str(e),
        }
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'offre: {str(e)}")
        return {
            "status": "error",
            "message": f"Une erreur est survenue: {str(e)}",
            "error": str(e),
        }


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
@inject
async def delete_job(
    job_id: str, job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        deleted = await job_writer.delete(job_id)
        if not deleted:
            return {
                "status": "success",
                "message": f"Aucune offre avec l'ID {job_id} n'a été trouvée, aucune suppression nécessaire",
            }
        return {
            "status": "success",
            "message": f"Offre d'emploi {job_id} supprimée avec succès",
        }
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'offre {job_id}: {str(e)}")
        return {
            "status": "error",
            "message": f"Une erreur est survenue lors de la suppression: {str(e)}",
            "error": str(e),
        }


# @router.post("/entreprises", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_entreprise(
#     entreprise: EntrepriseCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_entreprise(entreprise.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "L'entreprise existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création de l'entreprise: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}


# @router.post("/langues", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_langue(
#     langue: LangueCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_langue(langue.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "La langue existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création de la langue: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}


# @router.post("/durees-travail", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_duree_travail(
#     duree_travail: DureeTravailCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_duree_travail(duree_travail.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "La durée de travail existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création de la durée de travail: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}

# @router.post("/competences", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_competence(
#     competence: CompetenceCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_competence(competence.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "La compétence existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création de la compétence: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}

# @router.post("/modes-travail", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_mode_travail(
#     mode_travail: ModeTravailCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_mode_travail(mode_travail.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "Le mode de travail existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création du mode de travail: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}

# @router.post("/types-contrat", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_type_contrat(
#     type_contrat: TypeContratCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_type_contrat(type_contrat.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "Le type de contrat existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création du type de contrat: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}

# @router.post("/sources", status_code=status.HTTP_201_CREATED)
# @inject
# async def create_source(
#     source: SourceCreate,
#     job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
# ):
#     try:
#         result = await job_writer.add_source(source.libelle)
#         return {"status": "success", "id": result.id, "libelle": result.libelle}
#     except IntegrityError as e:
#         logger.warning(f"Erreur d'intégrité ignorée: {str(e)}")
#         if "duplicate key value violates unique constraint" in str(e):
#             return {"status": "success", "message": "La source existe déjà, aucune modification apportée"}
#         return {"status": "warning", "message": f"Problème d'intégrité des données: {str(e)}", "error": str(e)}
#     except Exception as e:
#         logger.error(f"Erreur lors de la création de la source: {str(e)}")
#         return {"status": "error", "message": f"Une erreur est survenue: {str(e)}", "error": str(e)}
