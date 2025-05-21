from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from app.domain.job.interfaces.ijob_repository import IJobRepository


router = APIRouter()

@router.get("/")
@inject
async def list_jobs(
    competence: str | None = None,
    repo: IJobRepository = Depends(Provide[ContainerService.job_repository]),
):
    try:
        return await repo.list(competence) # type: ignore
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get("/{job_id}", response_model=Job)
@inject
async def get_job(
    job_id: str,
    repo: IJobRepository = Depends(Provide[ContainerService.job_repository]),
):
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=Job, status_code=201)
@inject
async def add_job(
    job: Job,
    repo: IJobRepository = Depends(Provide[ContainerService.job_repository]),
):
    try:
        await repo.add(job)
        return job
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.delete("/{job_id}", status_code=204)
@inject
async def delete_job(
    job_id: str,
    repo: IJobRepository = Depends(Provide[ContainerService.job_repository]),
):
    if not await repo.delete(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
