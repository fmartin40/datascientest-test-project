from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date
from dependency_injector.wiring import inject, Provide
from app.core.container import ContainerService
from app.domain.job.interfaces.istat_reader import IStatsReader

router = APIRouter(tags=["stats"])


@router.get("/competences-by-date")
@inject
def list_competences_by_date(
    date_debut: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    date_fin: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    stats_reader: IStatsReader = Depends(Provide[ContainerService.stats_reader]),
):
    try:
        return stats_reader.list_competences_by_date(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/competence-by-date/{competence_id}")
@inject
async def get_competence_by_date(
    competence_id: int,
    date_debut: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    date_fin: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    stats_reader: IStatsReader = Depends(Provide[ContainerService.stats_reader]),
):
    try:
        return await stats_reader.get_competence_by_date(
            competence_id, date_debut, date_fin
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/sum-competences-by-date")
@inject
async def sum_competences_by_date(
    date_debut: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    date_fin: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    stats_reader: IStatsReader = Depends(Provide[ContainerService.stats_reader]),
):
    try:
        return await stats_reader.sum_competences_by_date(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
