from app.domain.profile.interfaces.ijob_repo import IJobRepo
from app.domain.profile.dtos.scrapjob import ScrapJobSummaryInputDto, ScrapJobDetailInputDto
from celery import Celery
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from app.core.container_service import ContainerService

router = APIRouter()


@router.post("/test/summaries")
@inject
async def list_jobs_summaries(
    input_dto: ScrapJobSummaryInputDto,
    dynamique:bool = False,
    celery_client: Celery = Depends(Provide[ContainerService.celery_client]),
):
    try:
        task_name = "dynamique.test_extract_summaries" if dynamique else "statique.test_extract_summaries"
        task = celery_client.send_task(
            task_name,  # Nom exact de la tâche
            kwargs=input_dto.model_dump()
        )
        
        return {"task_id": task.id, "status": "pending"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/test/detail")
@inject
async def get_job_detail(
    input_dto: ScrapJobDetailInputDto,
    dynamique:bool = False,
    celery_client: Celery = Depends(Provide[ContainerService.celery_client]),
):
    try:
        task_name = "dynamique.test_extract_jobdetail" if dynamique else "statique.test_extract_jobdetail"
        task = celery_client.send_task(
            task_name,  # Nom exact de la tâche
            kwargs=input_dto.model_dump(),
        )
        
        return {"task_id": task.id, "status": "pending"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/test/get-result/{task_id}")
@inject
async def get_result(task_id: str, job_repo: IJobRepo = Depends(Provide[ContainerService.job_repo])):
    try:
        result = await job_repo.get_job_detail(task_id)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Résultat non trouvé ou tâche en cours")
