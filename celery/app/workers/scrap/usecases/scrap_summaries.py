import asyncio
from typing import Optional
from app.core.container import ContainerService
from celery import shared_task, current_task
import logging
from app.workers.scrap.usecases.scrap_detail import extract_jobdetail

logger = logging.getLogger(__name__)

@shared_task(name="extract_summaries", queue="summaries_queue")
def extract_summaries(
    website: str,
    query: str,
    location: str,
    loop: int = 1,
    max_details: Optional[int] = None
):
    """
    Tâche qui extrait les résumés d'offres d'emploi et lance une tâche par URL trouvée.
    """
    try:
        logger.info(f"[{website}] Début de l'extraction - query: '{query}', location: '{location}', pages: {loop}")

        # Création du conteneur et récupération des services
        container = ContainerService()
        scraper_registry = container.scraper_registry()

        # Récupération du scraper
        scraper = scraper_registry.get_scraper(website)
        logger.info(f"[{website}] Scraper utilisé : {scraper.__class__.__name__}")

        # Exécution du scraper dans une boucle asyncio isolée
        summaries = asyncio.run(scraper.extract_summarize(query=query, location=location, loop=loop))
        logger.info(f"[{website}] {len(summaries)} résumés extraits")

        # Filtrage des résumés valides (avec URL)
        valid_summaries = [s for s in summaries if hasattr(s, 'url') and s.url]
        if max_details:
            valid_summaries = valid_summaries[:max_details]

        logger.info(f"[{website}] {len(valid_summaries)} tâches de détail à lancer")

        task_ids = []
        for i, summary in enumerate(valid_summaries[:5]):
            try:
                detail_task = extract_jobdetail.apply_async(
                    args=[summary.url, website],
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
                ) # type: ignore
                task_ids.append(detail_task.id)
                logger.info(f"[{website}] Tâche lancée pour : {summary.url}")
            except Exception as task_error:
                logger.error(f"[{website}] Échec de lancement pour URL: {summary.url} - {task_error}", exc_info=True)

        return {
            "summary_task_id": current_task.request.id,  # type: ignore
            "detail_task_ids": task_ids,
            "summary_count": len(summaries),
            "detail_count": len(task_ids)
        }

    except Exception as e:
        logger.error(f"[{website}] ERREUR dans extract_summaries: {e}", exc_info=True)
        raise
