from fastapi import APIRouter
from app.entrypoints.endpoint import jobs

routeur_job = APIRouter(prefix="/jobs", tags=["scrap"] )

routeur_job.include_router(jobs.router)

