from typing import Dict, List
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.core.container import ContainerService
from app.entrypoints.router import routeur_job   


# Instancier et configurer le container
endpoints: List[str] = [
    "app.entrypoints.endpoint.jobs"
]
container_service = ContainerService()
container_service.wire(modules=endpoints)


@asynccontextmanager
async def lifespan(app: FastAPI):
    es_client = container_service.es_client()
    if not await es_client.indices.exists(index="jobs"):
        es_index = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 768}
                }
            }
        }
        es_client.indices.create(index="jobs", body=es_index, ignore=[400])
    yield
    await es_client.close()


app = FastAPI(
    title="Api façade pour Elastic Search",
    description="""""",
    lifespan=lifespan
)

app.include_router(routeur_job)


# healthcheck dans le dockerfile
@app.get("/health")
def health_check():
    return {"status": "ok"}


