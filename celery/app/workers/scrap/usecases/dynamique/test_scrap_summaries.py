import asyncio
import logging
from typing import Dict
from app.core.container import ContainerService
from celery import shared_task, current_task

container = ContainerService()
scraper_registry = container.scraper_registry()
redis_loader = container.redis_loader()

logger = logging.getLogger(__name__)

@shared_task(name="dynamique.test_extract_summaries", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def extract_summaries_for_test(website: str, query: str, location: str, loop: int = 1):
    try:
        # Ajouter des logs plus détaillés
        logger.info(f"Démarrage de la tâche - website: {website}, query: {query}, location: {location}, loop: {loop}")
        
        # Créer une nouvelle boucle événementielle
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        
        try:
            # Récupérer le scraper via le registry
            scraper = scraper_registry.get_scraper(website)
            logger.info(f"Scraper récupéré: {scraper.__class__.__name__}")
            
            # Exécuter l'extraction de façon asynchrone
            logger.info(f"Démarrage de l'extraction des résumés - query: {query}, location: {location}")
            summaries = event_loop.run_until_complete(
                scraper.extract_summarize(query=query, location=location, loop=loop)
            )
            logger.info(f"Extraction terminée - Nombre de résumés: {len(summaries)}")
            
            # ID de la tâche Celery pour suivi dans Redis
            task_id: str = current_task.request.id  # type: ignore
            logger.info(f"Task ID: {task_id}")

            jobs: Dict = dict(
                task_id=task_id,
                website=website,
                query=query,
                location=location,
                loop=loop,
                summaries=[summary.model_dump() for summary in summaries]
            )
            
            logger.info(f"Données préparées pour Redis - nombre de résumés: {len(jobs['summaries'])}")
            
            # Insérer les données dans Redis
            logger.info(f"Insertion dans Redis avec task_id: {task_id}")
            redis_loader.insert(key=task_id, job=jobs)
            logger.info(f"Données insérées dans Redis - task_id: {task_id}")
            
            return task_id
        finally:
            # Fermer la boucle événementielle
            event_loop.close()

    except Exception as e:
        logger.error(f"ERREUR dans extract_summaries_for_test: {e}", exc_info=True)
        print(f"[ERROR] {e}")
        raise