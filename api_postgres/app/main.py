from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings

from app.core.container import ContainerService
from app.entrypoint.router import (
	routeur_job,
)


# Instancier et configurer le container UNE SEULE FOIS
endpoint = [
	'app.entrypoint.endpoint.jobs',
]
container_service = ContainerService()
container_service.wire(modules=endpoint)

# Définition de l'application FastAPI
app = FastAPI(
	title='Api postgres'
)

# Ajouter les routeurs
app.include_router(routeur_job)

# midleware pour forcer https
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.scheme == "http":
            # Force HTTPS pour les URLs générées
            response.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
        return response

# Ajouter ce middleware avant les autres
app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def safe_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Erreur serveur",
                "error": str(exc)  
            }
        )
    
 
     
# Connexion à MySQL via Tortoise
register_tortoise(
    app,
    db_url=f'asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST_DB}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}',
    modules={'models': ['app.infrastructure.models.models']},
    generate_schemas=False,
    add_exception_handlers=True,
)