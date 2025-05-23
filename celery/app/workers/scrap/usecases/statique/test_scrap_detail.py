import asyncio
from typing import Dict
import logging
from celery import shared_task, current_task
from app.core.container import ContainerService
from app.workers.scrap.entities.jobs import JobDetail
from app.infrastructure.statique.scraper import Scraper

container = ContainerService()
redis_loader = container.redis_loader()

logging.basicConfig(
    filename='worker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@shared_task(name="statique.test_extract_jobdetail", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def extract_jobdetail(url: str, source: str):
    try:
        logger.info(f"Début de l'extraction - url: {url}, source: {source}")
        
        # Créer une nouvelle boucle événementielle
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        
        try:
            # Récupérer le scraper via le registry
            scraper: Scraper = container.static_scrapers()[source] # type: ignore
            logger.info(f"Scraper récupéré: {scraper.__class__.__name__}")
            
            # Exécuter l'extraction et la transformation de façon asynchrone
            async def process_job():
                job_detail: JobDetail = await scraper.extract_detail(url=url) # type: ignore
                logger.info("Détails extraits avec succès")
                job_transformed: JobDetail = await scraper.transform(job_detail)
                logger.info("Job transformé avec succès")
                return job_detail, job_transformed
                
            job_detail, job_transformed = event_loop.run_until_complete(process_job())
            
            # ID de la tâche Celery pour suivi dans Redis
            task_id: str = current_task.request.id  # type: ignore
            logger.info(f"Task ID: {task_id}")
            
            job: Dict = dict(
                task_id=task_id,
                url=url,
                source=source,
                job_detail=job_detail.model_dump(),
            )
            
            # Insérer les données dans Redis
            logger.info(f"Insertion dans Redis avec task_id: {task_id}")
            redis_loader.insert(key=task_id, job=job)
            logger.info(f"Données insérées dans Redis - task_id: {task_id}")
            
            return task_id
        finally:
            # Fermer la boucle événementielle
            event_loop.close()

    except Exception as e:
        logger.error(f"ERREUR dans extract_jobdetail: {e}", exc_info=True)
        print(f"[ERROR] {e}")
        raise
