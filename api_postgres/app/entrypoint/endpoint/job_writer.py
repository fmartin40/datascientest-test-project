from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide
from app.core.container import ContainerService
from app.infrastructure.schemas.job_insert import (
    JobCreate, EntrepriseCreate, SalaireCreate, FormationCreate, 
    LangueCreate, ExperienceCreate, DureeTravailCreate, 
    CompetenceCreate, ModeTravailCreate, TypeContratCreate, SourceCreate
)
from app.infrastructure.job.job_writer import JobWriter

router = APIRouter(prefix="/jobs", tags=["write job infos"] )

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_job(
    job: JobCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        await job_writer.add(job)
        return {"status": "success", "message": "Offre d'emploi créée avec succès"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'offre: {str(e)}"
        )

@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
@inject
async def delete_job(
    job_id: str,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    deleted = await job_writer.delete(job_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offre d'emploi avec ID {job_id} non trouvée"
        )
    return {"status": "success", "message": f"Offre d'emploi {job_id} supprimée avec succès"}

@router.post("/entreprises", status_code=status.HTTP_201_CREATED)
@inject
async def create_entreprise(
    entreprise: EntrepriseCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_entreprise(entreprise)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'entreprise: {str(e)}"
        )

@router.post("/salaires", status_code=status.HTTP_201_CREATED)
@inject
async def create_salaire(
    salaire: SalaireCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_salaire(salaire)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du salaire: {str(e)}"
        )

@router.post("/formations", status_code=status.HTTP_201_CREATED)
@inject
async def create_formation(
    formation: FormationCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_formation(formation)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la formation: {str(e)}"
        )

@router.post("/langues", status_code=status.HTTP_201_CREATED)
@inject
async def create_langue(
    langue: LangueCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_langue(langue)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la langue: {str(e)}"
        )

@router.post("/experiences", status_code=status.HTTP_201_CREATED)
@inject
async def create_experience(
    experience: ExperienceCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_experience(experience)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'expérience: {str(e)}"
        )

@router.post("/durees-travail", status_code=status.HTTP_201_CREATED)
@inject
async def create_duree_travail(
    duree_travail: DureeTravailCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_duree_travail(duree_travail)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la durée de travail: {str(e)}"
        )

@router.post("/competences", status_code=status.HTTP_201_CREATED)
@inject
async def create_competence(
    competence: CompetenceCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_competence(competence)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la compétence: {str(e)}"
        )

@router.post("/modes-travail", status_code=status.HTTP_201_CREATED)
@inject
async def create_mode_travail(
    mode_travail: ModeTravailCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_mode_travail(mode_travail)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du mode de travail: {str(e)}"
        )

@router.post("/types-contrat", status_code=status.HTTP_201_CREATED)
@inject
async def create_type_contrat(
    type_contrat: TypeContratCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_type_contrat(type_contrat)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du type de contrat: {str(e)}"
        )

@router.post("/sources", status_code=status.HTTP_201_CREATED)
@inject
async def create_source(
    source: SourceCreate,
    job_writer: JobWriter = Depends(Provide[ContainerService.job_writer])
):
    try:
        result = await job_writer.add_source(source)
        return {"id": result.id, "libelle": result.libelle}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la source: {str(e)}"
        )
