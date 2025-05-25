import asyncio
from typing import Dict
import logging
from celery import shared_task, current_task
from app.core.container import ContainerService
from app.workers.scrap.entities.jobs import JobDetail

container = ContainerService()
scraper_registry = container.scraper_registry()
structured_db = container.structured_loader()
unstructured_db = container.unstructured_loader()

logger = logging.getLogger(__name__)

@shared_task(name="dynamique.extract_jobdetail", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def extract_jobdetail(url: str, website: str):
    """
    Tâche qui extrait les détails d'une offre d'emploi et les stocke en base.
    Cette tâche est consommée depuis la queue 'details_queue' de RabbitMQ.
    
    Args:
        url: L'URL de l'offre d'emploi
        website: Le site web source de l'offre
    
    Returns:
        Dict: Information sur la tâche exécutée
    """
    try:
        logger.info(f"Début de l'extraction - url: {url}, website: {website}")
        
        # Créer une nouvelle boucle événementielle
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        
        try:
            # Récupérer le scraper via le registry
            scraper = scraper_registry.get_scraper(website)
            logger.info(f"Scraper récupéré: {scraper.__class__.__name__}")
            
            # Exécuter l'extraction et la transformation de façon asynchrone
            async def process_job():
                try:
                    job_detail: JobDetail = await scraper.extract_detail(url=url) # type: ignore
                    logger.info("Détails extraits avec succès")
                    job_transformed: JobDetail = await scraper.transform(job_detail)
                    logger.info("Job transformé avec succès")
                    return job_detail, job_transformed
                except Exception as e:
                    logger.error(f"Erreur pendant le processus asynchrone: {e}", exc_info=True)
                    raise
                
            job_detail, job_transformed = event_loop.run_until_complete(process_job())
            
            # ID de la tâche Celery pour suivi dans Redis
            task_id: str = current_task.request.id  # type: ignore
            logger.info(f"Task ID: {task_id}")
            
            job: Dict = dict(
                task_id=task_id,
                url=url,
                website=website,
                job_detail=job_detail.model_dump(),
            )
            
            # Insérer les données dans les bases de données
            structured_db.insert(job=job_transformed) # type: ignore
            logger.info(f"Données insérées dans la base structurée pour l'URL: {url}")
            
            unstructured_db.insert(job=job_transformed) # type: ignore
            logger.info(f"Données insérées dans la base non structurée pour l'URL: {url}")
            
            return {
                'task_id': task_id,
                'url': url,
                'website': website,
                'status': 'success'
            }
        finally:
            # Fermer la boucle événementielle
            event_loop.close()

    except Exception as e:
        logger.error(f"ERREUR dans extract_jobdetail pour URL {url}: {e}", exc_info=True)
        print(f"[ERROR] {e}")
        # On relance l'exception pour déclencher le mécanisme de retry de Celery
        raise
