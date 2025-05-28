from typing import List
from fastapi import FastAPI
import asyncio
from fastapi.concurrency import asynccontextmanager
from app.core.container import ContainerService
from app.entrypoints.router import routeur_job_reader, routeur_job_writer
from app.core.config import settings
from app.infrastructure.initdb.fill_index import fill_index

# Instancier et configurer le container
endpoints: List[str] = [
    "app.entrypoints.endpoint.job_reader",
    "app.entrypoints.endpoint.job_writer",
]
container_service = ContainerService()
container_service.wire(modules=endpoints)


@asynccontextmanager
async def lifespan(app: FastAPI):
    opensearch_client = container_service.opensearch_client()
    index_name = settings.OPENSEARCH_JOB_INDEX
    loop = asyncio.get_running_loop()

    print(f"Vérification de l'index {index_name}...")

    try:
        exists = await loop.run_in_executor(
            None, lambda: opensearch_client.indices.exists(index=index_name)
        )
        if not exists:
            print(f"ATTENTION: L'index {index_name} n'existe pas! Création...")
            await loop.run_in_executor(
                None, lambda: opensearch_client.indices.create(index=index_name)
            )
            print(f"Index {index_name} créé avec succès")
            fill_index()
        else:
            count = await loop.run_in_executor(
                None, lambda: opensearch_client.count(index=index_name)
            )
            if count.get("count", 0) == 0:
                print(
                    f"Index {index_name} trouvé avec {count.get('count', 0)} documents"
                )
                print("Remplissage de l'index...")
                fill_index()
            else:
                print(
                    f"Index {index_name} trouvé avec {count.get('count', 0)} documents"
                )
    except Exception as e:
        print(f"Erreur de vérification de l'index: {e}")

    yield
    opensearch_client.close()


app = FastAPI(
    title="Api façade pour Elastic Search", description="""""", lifespan=lifespan  # type: ignore
)

app.include_router(routeur_job_reader)
app.include_router(routeur_job_writer)


# healthcheck dans le dockerfile
@app.get("/health")
def health_check():
    return {"status": "ok"}
