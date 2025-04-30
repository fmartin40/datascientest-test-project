import asyncio
from typing import Dict
import logging
from celery import shared_task, current_task
from app.core.container_service import ContainerService
from app.workers.common.entities.jobs import JobDetail
from app.infrastructure.pipelines.scraper_service import ScraperServices

container_service = ContainerService()

logging.basicConfig(
    filename='worker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@shared_task(name="test_extract_jobdetail")
def extract_jobdetail(url: str, website: str):
    try:
        logger.info("Début de l'extraction")
        scrap_settings = (
            container_service.website_settings_loader().load_website_settings(website)
        )
        scraper: ScraperServices = container_service.scrap_services(
            scrap_settings=scrap_settings
        )
        job_detail: JobDetail = asyncio.run(scraper.extract_detail(url=url))  # type: ignore
        job_transformed: JobDetail = asyncio.run(scraper.transform(job_detail))
        logger.info(f"Job transformé : {job_transformed}")
       
        # Id de la task pour redis
        task_id: str = current_task.request.id  # type: ignore
        job: Dict = dict(
            task_id=task_id,
            url=url,
            website=website,
            job_detail=job_detail.model_dump(),
            
        )
        asyncio.run(container_service.redis_detail().insert(key=task_id, job=job))
        # return [summary.model_dump(mode="json") for summary in summaries]

    except Exception as e:
        print(e)
        raise
