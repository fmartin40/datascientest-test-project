from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide
import asyncio
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from app.domain.job.interfaces.ijob_writer import IJobWriter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs")


@router.post("/create", status_code=status.HTTP_201_CREATED)
@inject
async def add_job(
    job: Job,
    repo: IJobWriter = Depends(Provide[ContainerService.job_writer_opensearch]),
):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, repo.add, job)
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
@inject
async def delete_job(
    job_id: str,
    repo: IJobWriter = Depends(Provide[ContainerService.job_writer_opensearch]),
):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, repo.delete, job_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
