from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings
import logging
import os

from app.core.container import ContainerService
from app.entrypoint.router import (
    routeur_job_reader,
    routeur_job_writer,
    routeur_mappings,
    routeur_stats,
)


# Chemin absolu pour le fichier de log
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "postgres.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8"), logging.StreamHandler()],
)


# Active les logs SQL de Tortoise
logging.getLogger("tortoise").setLevel(logging.DEBUG)

# Instancier et configurer le container UNE SEULE FOIS
endpoint = [
    "app.entrypoint.endpoint.job_reader",
    "app.entrypoint.endpoint.job_writer",
    "app.entrypoint.endpoint.mappings",
    "app.entrypoint.endpoint.stats",
]
container_service = ContainerService()
container_service.wire(modules=endpoint)

# Définition de l'application FastAPI
app = FastAPI(title="Api postgres")

# Ajouter les routeurs
app.include_router(routeur_job_reader)
app.include_router(routeur_job_writer)
app.include_router(routeur_mappings)
app.include_router(routeur_stats)


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
            status_code=500, content={"detail": "Erreur serveur", "error": str(exc)}
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


# Connexion à MySQL via Tortoise
register_tortoise(
    app,
    db_url=f"asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    modules={"models": ["app.infrastructure.models.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
