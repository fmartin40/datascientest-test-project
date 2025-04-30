from typing import List
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
                    "job_id": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "website": {"type": "keyword"},
                    "title": {"type": "keyword"},
                    "company": {"type": "keyword"},
                    "city": {"type": "keyword"},
                    "postal_code": {"type": "integer"},
                    "contract_type": {"type": "keyword"},
                    "description": {"type": "text"},
                    "infos": {"type": "nested", "properties": {
                        "technologies": {"type": "keyword"},
                        "embeddings": {"type": "dense_vector", "dims": 768}
                    }}
                }
            }
        }
        await es_client.indices.create(index="jobs", body=es_index)
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


