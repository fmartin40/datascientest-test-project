from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date
from dependency_injector.wiring import inject, Provide
from app.core.container import ContainerService
from app.domain.job.interfaces.istat_reader import IStatsReader
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["stats"])


@router.get("/competences/daily")
@inject
async def list_competences_by_day(
    from_date: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    to_date: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    stats_reader: IStatsReader = Depends(Provide[ContainerService.stats_reader]),
):
    try:
        return await stats_reader.list_competences_by_day(from_date, to_date)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des compétences par date: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/competences/sum")
@inject
async def get_competence_by_date(
    competence_id: int | None = Query(None, description="ID de la compétence"),
    from_date: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    to_date: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    stats_reader: IStatsReader = Depends(Provide[ContainerService.stats_reader]),
):
    try:
        return await stats_reader.sum_competences_by_date(
            from_date, to_date, competence_id
        )

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des compétences par date: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
