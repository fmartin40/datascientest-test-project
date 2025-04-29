import asyncio
from typing import Dict, List
from app.core.container_service import ContainerService
from app.workers.common.entities.jobs import JobSummary
from celery import shared_task, current_task

container_service = ContainerService()


@shared_task(name="test_extract_summaries")
def extract_summaries(website: str, query: str, location: str, loop: int = 1):
    try:
        scrap_settings = (
            container_service.website_settings_loader().load_website_settings(website)
        )
        summaries: List[JobSummary] = asyncio.run(
            container_service.scrap_services(
                scrap_settings=scrap_settings
            ).extract_summarize(query=query, location=location, loop=loop)
        )
        # Id de la task pour redis
        task_id: str =current_task.request.id # type: ignore
        jobs: Dict=dict(
            task_id=task_id,
            website=website,
            query=query,
            location=location,
            loop=loop,
            summaries=[summary.model_dump() for summary in summaries] # type: ignore
        )
        asyncio.run(
            container_service.redis_summaries().insert(key=task_id, jobs=jobs)
        )
        # return [summary.model_dump(mode="json") for summary in summaries]

    except Exception as e:
        print(e)
        raise
