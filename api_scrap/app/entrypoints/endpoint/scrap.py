from dataclasses import asdict
from typing import Any, Dict
from app.domain.scrap.dtos.scrapjob import ScrapJobSummaryInputDto, ScrapJobDetailInputDto
from celery import Celery
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from app.core.container_service import ContainerService

router = APIRouter()

# Une simple base de données en mémoire pour stocker les résultats
# Dans un cas réel, vous utiliseriez une base de données persistante
scraping_results = {}


class ScrapingResult(BaseModel):
    task_id: str
    status: str
    data: Dict[str, Any]


@router.post("/jobs/summaries")
@inject
async def list_jobs_summaries(
    input_dto: ScrapJobSummaryInputDto,
    celery_client: Celery = Depends(Provide[ContainerService.celery_client]),
):
    try:
        task = celery_client.send_task(
            "extract_summaries",  # Nom exact de la tâche
            kwargs=input_dto.model_dump()
        )
        
        return {"task_id": task.id, "status": "pending"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/jobs/detail")
@inject
async def get_job_detail(
    input_dto: ScrapJobDetailInputDto,
    celery_client: Celery = Depends(Provide[ContainerService.celery_client]),
):
    try:
        task = celery_client.send_task(
            "extract_jobdetail",  # Nom exact de la tâche
            kwargs=input_dto.model_dump(),
        )
        
        return {"task_id": task.id, "status": "pending"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

