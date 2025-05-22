from fastapi import APIRouter
from app.entrypoints.endpoint import job_writer, job_reader

routeur_job_reader = APIRouter(tags=["jobs reader"] )
routeur_job_reader.include_router(job_reader.router)

routeur_job_writer = APIRouter(tags=["jobs writer"] )
routeur_job_writer.include_router(job_writer.router)
