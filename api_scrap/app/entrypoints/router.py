from fastapi import APIRouter
from app.entrypoints.endpoint import pipelines

routeur_pipelines = APIRouter()
# routeur_search = APIRouter()

routeur_pipelines.include_router(pipelines.router)
