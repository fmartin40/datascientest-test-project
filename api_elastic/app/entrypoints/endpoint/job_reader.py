from fastapi import APIRouter, HTTPException, status, Depends, Query
from dependency_injector.wiring import inject, Provide
import asyncio

# from app.infrastructure.opensearch.job_reader import JobReaderOpenSearch
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from app.domain.job.interfaces.ijob_reader import IJobReader

# from app.infrastructure.sessions.opensearch_session import get_opensearch_client

router = APIRouter(prefix="/jobs")


@router.get("/search")
@inject
async def search_jobs_by_description(
    q: str = Query(..., description="Texte à rechercher dans la description"),
    repo: IJobReader = Depends(Provide[ContainerService.job_reader_opensearch]),
):
    try:
        # loop = asyncio.get_running_loop()
        print("eeeeeeeeeeeeee")
        return "eeeeeeeeeeeeee"
        #   job = await repo.search_by_description(q)
        # return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
@inject
async def list_jobs(
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=30),
    repo: IJobReader = Depends(Provide[ContainerService.job_reader_opensearch]),
):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, repo.list, offset, limit)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/ids")
@inject
async def list_by_ids(
    job_ids: str,
    repo: IJobReader = Depends(Provide[ContainerService.job_reader_opensearch]),
):
    loop = asyncio.get_running_loop()
    ids = job_ids.split(",")
    job = await loop.run_in_executor(None, repo.list_by_ids, ids)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}", response_model=Job)
@inject
async def get_job(
    job_id: str,
    repo: IJobReader = Depends(Provide[ContainerService.job_reader_opensearch]),
):
    loop = asyncio.get_running_loop()
    job = await loop.run_in_executor(None, repo.get, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
