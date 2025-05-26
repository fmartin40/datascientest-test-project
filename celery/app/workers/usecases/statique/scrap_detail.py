import asyncio
from typing import List, Dict
import logging
import hashlib
from celery import shared_task, current_task
from app.core.container import ContainerService
from app.workers.entities.jobs import JobDetail, JobSummary
from app.workers.interfaces.istatic_extractor import IStaticExtractor
# from app.core.nlp import COMPETENCES, MODE_TRAVAIL, TYPE_CONTRAT, DUREE_TRAVAIL

container = ContainerService()
elastic_loader = container.unstructured_loader()
postgres_loader = container.structured_loader()
redis_loader = container.redis_loader()

logging.basicConfig(
    filename="worker.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@shared_task(
    name="statique.extract_jobdetail",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def extract_jobdetail(summary: dict, source: str):
    try:
        task_id: str = current_task.request.id  # type: ignore
        logger.info(
            f"Début de l'extraction detail - job_summary: {summary}, source: {source}, Task ID: {task_id}"
        )
        
        # ----- lancement du process de scrap
        scraper: IStaticExtractor = container.scraper_factory()[source]  # type: ignore
        job_detail: JobDetail = asyncio.run(
            scraper.extract_details(job_summary=JobSummary(**summary))
        )  # type: ignore
        logger.info(f"Détails extraits avec succès : {job_detail}")

        # ----- génération de l'id du job
        combined = f"{job_detail.description.strip().lower()}|{job_detail.libelle.strip().lower()}"
        job_detail.job_id = hashlib.sha256(combined.encode()).hexdigest()
        
        # # # ----- Insertion des données dans Elasticsearch
        asyncio.run(elastic_loader.insert(job_detail))

        # # # ----- Insertion des données dans PostgreSQL
        asyncio.run(postgres_loader.insert(job_detail))

        # ----- Insertion des données dans Redis
        redis_loader.insert(key=task_id, job=[job_detail.model_dump()], ttl=300)
        logger.info(f"job detail insérées dans Redis - task_id: {task_id}")
        logger.info(f"traitement terminé - job detail: {job_detail.model_dump()}")
        return job_detail.model_dump()

    except Exception as e:
        logger.error(f"ERREUR dans extract_jobdetail: {e}", exc_info=True)
        print(f"[ERROR] {e}")
        raise


# async def transform_job_detail(job_detail: JobDetail):
#     try:
#         keywords_loader = container.keywords_loader()
#         if job_detail.competence is None:
#             keywords_competences: Dict[str, int] = await keywords_loader.load_competences() # type: ignore
#             job_detail.competence = await container.keyword_transformer(mapping=keywords_competences).transform(text=job_detail.description, type="liste") # type: ignore
        
#         if job_detail.mode_travail is None:
#             keywords_mode_travail: Dict[str, int] = await keywords_loader.load_mode_travail() # type: ignore
#             job_detail.mode_travail = await container.keyword_transformer(mapping=keywords_mode_travail).transform(text=job_detail.description, type="keyword") # type: ignore
        
#         if job_detail.type_contrat is None:
#             keywords_type_contrat: Dict[str, int] = await keywords_loader.load_type_contrat() # type: ignore
#             job_detail.type_contrat = await container.keyword_transformer(mapping=keywords_type_contrat).transform(text=job_detail.description, type="keyword") # type: ignore
        
#         if job_detail.duree_travail is None:
#             keywords_duree_travail: Dict[str, int] = await keywords_loader.load_duree_travail() # type: ignore
#             job_detail.duree_travail = await container.keyword_transformer(mapping=keywords_duree_travail).transform(text=job_detail.description, type="keyword") # type: ignore
        
#         logger.info(f"job_detail transformé: {job_detail.model_dump()}")
#         return job_detail
#     except Exception as e:
#         logger.error(f"ERREUR dans transform_job_detail: {e}", exc_info=True)
#         raise
