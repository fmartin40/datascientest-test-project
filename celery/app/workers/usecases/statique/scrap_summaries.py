import asyncio
import logging
from typing import Dict, List
from app.core.container import ContainerService
from celery import shared_task, current_task
from app.workers.usecases.statique.scrap_detail import extract_jobdetail
from app.workers.entities.jobs import JobSummary
from app.workers.interfaces.istatic_extractor import IStaticExtractor

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
    name="statique.extract_summaries",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def extract_summaries(
    source: str,
    query: str,
    location: str,
    loop: int = 1,
) -> Dict:
    try:
        task_id: str = current_task.request.id  # type: ignore
        logger.info(
            f"[START] source={source}, query={query}, location={location}, loop={loop}"
        )

        # ---- extraction des job summaries
        scraper: IStaticExtractor = container.scraper_factory()[source]  # type: ignore
        job_summaries: List[JobSummary] = run_async(
            scraper.extract_summaries(query=query, location=location, loop=loop)
        )
        logger.info(f"Résumés extraits: {len(job_summaries)}")

        job_summaries = job_summaries[:1]


        # ---- lancement des tâches job details pour les job summaries avec URL valide
        launch_job_detail_tasks(
            job_summaries=[s for s in job_summaries if s.url], source=source
        )

        # ---- stockage des job_summary dans Redis
        redis_loader.insert(key=task_id, job=[s.model_dump() for s in job_summaries], ttl=300)
        logger.info(f"Résumés stockés dans Redis : {task_id}")
        
        return {
            "task_id": task_id,
            "source": source,
            "query": query,
            "location": location,
            "loop": loop,
            "job_summaries_count": len(job_summaries),
            "job_summaries": [s.model_dump() for s in job_summaries],
        }

    except Exception as e:
        logger.error(f"[FATAL] Erreur dans extract_summaries : {e}", exc_info=True)
        raise

def launch_job_detail_tasks(job_summaries: List[JobSummary], source: str):
    try:
        task_ids = []
        print(f"job_summaries: {job_summaries}")
 
        for i, job_summary in enumerate(job_summaries):
            detail_task = extract_jobdetail.apply_async(
                kwargs={
                    "summary": job_summary.model_dump(),
                    "source": source,
                },
                countdown=2 * i,
                expires=3600,
                retry=True,
                retry_policy={
                    "max_retries": 3,
                    "interval_start": 0,
                    "interval_step": 60,
                    "interval_max": 300,
                },
            )  # type: ignore
            task_ids.append(detail_task.id)
            logger.info(f"Tâche détail lancée pour : {job_summary.url}")
    except Exception as task_error:
        logger.error(
            f"Erreur tâche détail ({job_summary.url}): {task_error}", exc_info=True
        )

