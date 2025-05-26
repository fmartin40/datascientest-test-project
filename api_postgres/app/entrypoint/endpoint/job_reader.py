from fastapi import APIRouter, HTTPException, status, Depends, Query
from dependency_injector.wiring import inject, Provide
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from typing import Optional
from app.infrastructure.job.job_reader import JobReader

router = APIRouter(tags=["read job infos"])

@router.get("/jobs", response_model=list[Job])
@inject
async def list_jobs(
    limit: int = Query(30, ge=1, le=30),
    offset: int = Query(0, ge=0),
    competence: Optional[int] = Query(None),
    langue: Optional[int] = Query(None),
    entreprise: Optional[int] = Query(None),
    ville: Optional[int] = Query(None),
    type_contrat: Optional[int] = Query(None),
    duree_travail: Optional[int] = Query(None),
    mode_travail: Optional[int] = Query(None),
    source: Optional[int] = Query(None),
    light: bool = Query(True),
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list(
            competence=competence,
            entreprise=entreprise,
            ville=ville,
            type_contrat=type_contrat,
            duree_travail=duree_travail,
            mode_travail=mode_travail,
            source=source,
            light=light,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des offres"
        )

@router.get("/jobs/{job_id}", response_model=Job)
@inject
async def get_job(
    job_id: str,
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/competences")
@inject
async def list_competences(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_competences()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des compétences: {str(e)}"
        )



@router.get("/entreprises")
@inject
async def list_entreprises(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_entreprises()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des entreprises: {str(e)}"
        )

@router.get("/types-contrat")
@inject
async def list_types_contrat(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_type_contrat()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des types de contrat: {str(e)}"
        )

@router.get("/duree-travail")
@inject
async def list_duree_travail(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_duree_travail()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des durées de travail: {str(e)}"
        )

@router.get("/mode-travail")    
@inject
async def list_mode_travail(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_mode_travail()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des modes de travail: {str(e)}"
        )   

@router.get("/sources")
@inject
async def list_sources(
    repo: JobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list_source()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des sources: {str(e)}"
        )

