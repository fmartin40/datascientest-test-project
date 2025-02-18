from fastapi import APIRouter
from app.entrypoints.endpoint import pipelines, jobsearch

routeur_pipelines = APIRouter()
routeur_search = APIRouter()

routeur_pipelines.include_router(pipelines.router)
routeur_pipelines.include_router(jobsearch.router)