from fastapi import APIRouter
from app.entrypoints.endpoint import scrap
from app.entrypoints.endpoint import profile

routeur_scrap = APIRouter(prefix="/scrap", tags=["scrap"] )
routeur_profile = APIRouter(prefix="/profile", tags=["profile"] )

routeur_scrap.include_router(scrap.router)
routeur_profile.include_router(profile.router)
