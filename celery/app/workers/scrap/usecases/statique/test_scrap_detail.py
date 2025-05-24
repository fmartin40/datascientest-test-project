import asyncio
from typing import Dict
import logging
from celery import shared_task, current_task
from app.core.container import ContainerService
from app.workers.scrap.entities.jobs import JobDetail, JobSummary
from app.workers.scrap.interfaces.istatic_extractor import IStaticExtractor
from app.workers.scrap.interfaces.itransformer import ITransformer

container = ContainerService()
redis_loader = container.redis_loader()

logging.basicConfig(
    filename="worker.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@shared_task(
    name="statique.test_extract_jobdetail",
    # autoretry_for=(Exception,),
    # retry_kwargs={"max_retries": 3, "countdown": 60},
)
def test_extract_jobdetail(summary: dict, source: str):
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

        # ----- lancement des transformations
        # job_detail = asyncio.run(
        #     container.competence_transformer().transform(job_detail))
        # job_detail = asyncio.run(
        #     container.mode_travail_transformer().transform(job_detail))
        # job_detail = asyncio.run(
        #     container.type_contrat_transformer().transform(job_detail))
        # logger.info("Transformations effectuées avec succès")

        # # ----- Insertion des données dans Redis
        # redis_loader.insert(key=task_id, job=[job_detail.model_dump()], ttl=300)
        # logger.info(f"job detail insérées dans Redis - task_id: {task_id}")
        # return task_id
        

    except Exception as e:
        logger.error(f"ERREUR dans extract_jobdetail: {e}", exc_info=True)
        print(f"[ERROR] {e}")
        raise


# Exécuter l'extraction et la transformation de façon asynchrone
async def extract_job_detail(scraper: IStaticExtractor, job_summary: JobSummary):
    try:
        job_detail: JobDetail = await scraper.extract_detail(job_summary=job_summary)  # type: ignore
        logger.info(f"Détails extraits avec succès : {job_detail.model_dump()}")
        return job_detail
    except Exception as e:
        logger.error(f"ERREUR dans process_job: {e}", exc_info=True)
        raise


async def transform_job_detail(transformer: ITransformer, job_detail: JobDetail):
    try:
        job_transformed: JobDetail = await transformer.transform(job_detail)
        logger.info("Job transformé avec succès")
        return job_transformed
    except Exception as e:
        logger.error(f"ERREUR dans transform_job_detail: {e}", exc_info=True)
        raise
