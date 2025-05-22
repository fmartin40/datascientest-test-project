from typing import List
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.core.container import ContainerService
from app.entrypoints.router import routeur_job_reader, routeur_job_writer   
from app.core.config import settings


# Instancier et configurer le container
endpoints: List[str] = [
    "app.entrypoints.endpoint.job_reader",
    "app.entrypoints.endpoint.job_writer"
]
container_service = ContainerService()
container_service.wire(modules=endpoints)


@asynccontextmanager
async def lifespan(app: FastAPI):
    es_client = container_service.es_client()

    index_name = settings.ELASTIC_INDEX
    print(f"Vérification de l'index {index_name}...")
    
    if not await es_client.indices.exists(index=index_name):
        print(f"ATTENTION: L'index {index_name} n'existe pas!")
        print(f"L'index {index_name} devrait être créé par le script d'initialisation d'Elasticsearch.")
        print("Vérifiez que le conteneur elasticsearch a bien démarré et que le script insert_data.sh a été exécuté.")
    else:
        print(f" Index {index_name} trouvé")
        count = await es_client.count(index=index_name)
        print(f"Nombre de documents: {count.get('count', 0)}")
    
    yield
    await es_client.close()


app = FastAPI(
    title="Api façade pour Elastic Search",
    description="""""",
    lifespan=lifespan
)

app.include_router(routeur_job_reader)
app.include_router(routeur_job_writer)


# healthcheck dans le dockerfile
@app.get("/health")
def health_check():
    return {"status": "ok"}


