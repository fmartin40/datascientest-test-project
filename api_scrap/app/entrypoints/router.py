from fastapi import APIRouter
from app.entrypoints.endpoint import scrap

routeur_pipelines = APIRouter()
# routeur_search = APIRouter()

routeur_pipelines.include_router(scrap.router)
