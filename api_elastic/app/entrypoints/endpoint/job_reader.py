from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from app.domain.job.interfaces.ijob_reader import IJobReader


router = APIRouter(prefix="/jobs")

@router.get("/")
@inject
async def list_jobs(
    repo: IJobReader = Depends(Provide[ContainerService.job_reader]),
):
    try:
        return await repo.list()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get("/{job_id}", response_model=Job)
@inject
async def get_job(
    job_id: str,
    repo: IJobReader = Depends(Provide[ContainerService.job_reader]),
):
    job = await repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
