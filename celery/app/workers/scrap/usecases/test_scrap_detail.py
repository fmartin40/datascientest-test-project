import asyncio
from typing import Dict
import logging
from celery import shared_task, current_task
from app.core.container import ContainerService
from app.workers.scrap.entities.jobs import JobDetail

container = ContainerService()
scraper_registry = container.scraper_registry()
redis_loader = container.redis_loader()

logging.basicConfig(
    filename='worker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@shared_task(name="test_extract_jobdetail")
def extract_jobdetail_for_test(url: str, website: str):
    try:
        logger.info("Début de l'extraction")
        
        async def process_job():
            # Récupérer le scraper via le registry (avec config à jour automatiquement)
            scraper = scraper_registry.get_scraper(website)

            job_detail: JobDetail = await scraper.extract_detail(url=url)  # type: ignore
            job_transformed: JobDetail = await scraper.transform(job_detail)
            logger.info(f"Job transformé : {job_transformed}")
           
            # Id de la task pour redis
            task_id: str = current_task.request.id  # type: ignore
            job: Dict = dict(
                task_id=task_id,
                url=url,
                website=website,
                job_detail=job_detail.model_dump(),
            )
            return task_id, job

        # Exécuter toutes les opérations asynchrones dans une seule boucle
        task_id, job =asyncio.run(process_job())

        print('job ============================', job)
        redis_loader.insert(key=task_id, job=job)

    except Exception as e:
        logger.error(f"Erreur lors de l'extraction: {str(e)}")
        raise
