from typing import Dict, List
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.core.container import ContainerService
from app.entrypoints.router import routeur_job   


# Instancier et configurer le container
endpoints: List[str] = [
    "app.entrypoints.endpoint.jobs"
]
container_service = ContainerService()
container_service.wire(modules=endpoints)
es_client = container_service.es_client()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await container_service.init_resources()
    yield
    await es_client.close()


app = FastAPI(
    title="Api façade pour Elastic Search",
    description="""""",
    # lifespan=lifespan
)

app.include_router(routeur_job)



# healthcheck dans le dockerfile
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint pour afficher toutes les routes existantes
@app.get("/routes/", response_model=List[Dict])
async def get_routes():
    routes_info = []

    for route in app.routes:
        # On filtre les routes de type 'HTTPRoute' pour éviter les WebSocket ou autres types de routes
        if hasattr(route, "methods"):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name,
            })
    return routes_info

