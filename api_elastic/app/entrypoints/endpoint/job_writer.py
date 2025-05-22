from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide
from app.domain.job.entities.jobs import Job
from app.core.container import ContainerService
from app.domain.job.interfaces.ijob_writer import IJobWriter


router = APIRouter(prefix="/jobs")
    

@router.post("/", response_model=Job, status_code=201)
@inject
async def add_job(
    job: Job,
    repo: IJobWriter = Depends(Provide[ContainerService.job_writer]),
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
    repo: IJobWriter = Depends(Provide[ContainerService.job_writer]),
):
    if not await repo.delete(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
