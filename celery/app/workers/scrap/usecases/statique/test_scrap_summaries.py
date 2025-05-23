import asyncio
import logging
from typing import Dict, Optional, List
from app.core.container import ContainerService
from celery import shared_task, current_task
from app.infrastructure.statique.scraper import Scraper
from app.workers.scrap.usecases.statique.test_scrap_detail import extract_jobdetail

logger = logging.getLogger(__name__)
container = ContainerService()
redis_loader = container.redis_loader()

def run_async(coro):
    """Lance une coroutine dans une nouvelle boucle asyncio."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@shared_task(
    name="statique.test_extract_summaries",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60}
)
def extract_summaries(source: str, query: str, location: str, loop: int = 1, max_details: Optional[int] = None) -> Dict:
    try:
        logger.info(f"[START] source={source}, query={query}, location={location}, loop={loop}")
        
        scraper: Scraper = container.static_scrapers()[source]  # type: ignore
        logger.info(f"Scraper utilisé: {scraper.__class__.__name__}")

        # Exécuter l'extraction asynchrone
        summaries = run_async(scraper.extract_summarize(query=query, location=location, loop=loop))
        logger.info(f"Résumés extraits: {len(summaries)}")

        task_id: str = current_task.request.id  # type: ignore

        jobs: Dict = {
            "task_id": task_id,
            "source": source,
            "query": query,
            "location": location,
            "loop": loop,
            "summaries": [s.model_dump() for s in summaries]
        }

        redis_loader.insert(key=task_id, job=jobs)
        logger.info(f"Résumés stockés dans Redis : {task_id}")

        # Filtrage des résumés avec URL valide
        valid_summaries = [s for s in summaries if getattr(s, 'url', None)]
        if max_details:
            valid_summaries = valid_summaries[:max_details]

        logger.info(f"{len(valid_summaries)} tâches de détail à lancer")

        task_ids = []
        for i, summary in enumerate(valid_summaries):
            try:
                detail_task = extract_jobdetail.apply_async(
                    args=[summary.url, source],
                    queue='details_queue',
                    countdown=2 * i,
                    expires=3600,
                    retry=True,
                    retry_policy={
                        'max_retries': 3,
                        'interval_start': 0,
                        'interval_step': 60,
                        'interval_max': 300,
                    }
                )  # type: ignore
                task_ids.append(detail_task.id)
                logger.info(f"Tâche détail lancée pour : {summary.url}")
            except Exception as task_error:
                logger.error(f"Erreur tâche détail ({summary.url}): {task_error}", exc_info=True)

        return {
            "summary_task_id": task_id,
            "detail_task_ids": task_ids,
            "summary_count": len(summaries),
            "detail_count": len(task_ids)
        }

    except Exception as e:
        logger.error(f"[FATAL] Erreur dans extract_summaries : {e}", exc_info=True)
        raise
