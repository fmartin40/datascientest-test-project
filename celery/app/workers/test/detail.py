import asyncio
from typing import Dict
from celery import shared_task, current_task
from app.core.container_service import ContainerService
from app.workers.common.entities.jobs import JobDetail
container_service = ContainerService()

@shared_task(name="test_extract_jobdetail")
def extract_jobdetail(url: str, website: str):
    try:
        scrap_settings = (
            container_service.website_settings_loader().load_website_settings(website)
        )
        job_detail: JobDetail = asyncio.run(
            container_service.scrap_services(
                scrap_settings=scrap_settings
            ).extract_detail(url=url)
        ) # type: ignore

        # Id de la task pour redis
        task_id: str =current_task.request.id # type: ignore
        job: Dict=dict(
            task_id=task_id,
            url=url,
            website=website,
            job_detail=job_detail.model_dump()
        )
        asyncio.run(
            container_service.redis_detail().insert(key=task_id, job=job)
        )
        # return [summary.model_dump(mode="json") for summary in summaries]

    except Exception as e:
        print(e)
        raise

