import asyncio
from typing import Dict, List
from app.core.container import ContainerService
from app.workers.scrap.entities.jobs import JobSummary
from celery import shared_task, current_task

container = ContainerService()
scraper_registry = container.scraper_registry()


@shared_task(name="test_extract_summaries")
def extract_summaries_for_test(website: str, query: str, location: str, loop: int = 1):
    try:
        async def process_job():
            
            # Récupérer le scraper via le registry (avec config à jour automatiquement)
            scraper = scraper_registry.get_scraper(website)

            # Exécuter l'extraction
            summaries: List[JobSummary] = asyncio.run(
                scraper.extract_summarize(query=query, location=location, loop=loop)
            )

            # ID de la tâche Celery pour suivi dans Redis
            task_id: str = current_task.request.id  # type: ignore

            jobs: Dict = dict(
                task_id=task_id,
                website=website,
                query=query,
                location=location,
                loop=loop,
                summaries=[summary.model_dump() for summary in summaries]
            )
            
            


    except Exception as e:
        print(f"[ERROR] {e}")
        raise