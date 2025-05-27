from fastapi import APIRouter, HTTPException, status, Depends, Query
from dependency_injector.wiring import inject, Provide
from app.core.container import ContainerService
from app.domain.job.interfaces.imappings import IMappings
import logging

router = APIRouter(prefix="/mappings", tags=["mappings"])
logger = logging.getLogger(__name__)


@router.get("/types-contrat")
@inject
async def list_types_contrat(
    repo: IMappings = Depends(Provide[ContainerService.mappings]),
):
    try:
        response = await repo.list_type_contrat()
        logging.info(f"Réponse des types de contrat: {response}")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/mode-travail")
@inject
async def list_mode_travail(
    repo: IMappings = Depends(Provide[ContainerService.mappings]),
):
    try:
        return await repo.list_mode_travail()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/duree-travail")
@inject
async def list_duree_travail(
    repo: IMappings = Depends(Provide[ContainerService.mappings]),
):
    try:
        return await repo.list_duree_travail()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/competences")
@inject
async def list_competences(
    repo: IMappings = Depends(Provide[ContainerService.mappings]),
):
    try:
        return await repo.list_competence()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/villes")
@inject
async def list_villes(
    repo: IMappings = Depends(Provide[ContainerService.mappings]),
):
    try:
        return await repo.list_ville()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
