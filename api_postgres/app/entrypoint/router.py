from fastapi import APIRouter
from app.entrypoint.endpoint import job_reader, job_writer, mappings, stats

routeur_job_reader = APIRouter(tags=["read job infos"])
routeur_job_writer = APIRouter(tags=["write job infos"])
routeur_mappings = APIRouter(tags=["mappings"])
routeur_stats = APIRouter(tags=["stats"])

routeur_job_reader.include_router(job_reader.router)
routeur_job_writer.include_router(job_writer.router)
routeur_mappings.include_router(mappings.router)
routeur_stats.include_router(stats.router)
