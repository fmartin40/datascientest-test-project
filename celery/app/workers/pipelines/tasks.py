import asyncio
from typing import List
from app.core.container_service import ContainerService
from app.workers.pipelines.entities.jobs import JobDetail, JobSummary
from app.main import celery_client
import requests

container_service = ContainerService()

FASTAPI_WEBHOOK_URL = "http://localhost:8000/pipelines/webhook/scraping-result"


@celery_client.task(name="extract_summaries")
def extract_summaries(website: str, query: str, location: str, loop: int = 1):
    try:
        summaries: List[JobSummary] = asyncio.run(
            container_service.scrap_services_provider(
                scrap_settings=container_service.website_settings_loader().load_website_settings(
                    website
                )
            ).extract_summarize(query=query, location=location, loop=loop)
        )

        # Appel au webhook FastAPI
        response = requests.post(
            FASTAPI_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json={
                "task_id": extract_summaries.request.id,
                "status": "completed",
                "data": {
                    "summaries": [
                        summary.model_dump(mode="json") for summary in summaries
                    ]
                },
            },
        )

        # Vérifier si l'envoi a réussi
        if response.status_code != 200:
            print(f"Échec d'envoi au webhook: {response.text}")

        return [summary.model_dump(mode="json") for summary in summaries]

    except Exception as e:
        # En cas d'erreur, envoyez également l'information au webhook
        error_result = {
            "task_id": extract_summaries.request.id,
            "status": "failed",
            "data": {"error": str(e)},
        }

        try:
            requests.post(
                FASTAPI_WEBHOOK_URL,
                json=error_result,
                headers={"Content-Type": "application/json"},
            )
        except:
            pass  # Ignorer les erreurs lors de la notification d'erreur

        raise


@celery_client.task(name="extract_jobdetail")
def extract_jobdetail(url: str, website: str):
    try:
        jobdetail: JobDetail = asyncio.run(
            container_service.scrap_services_provider(
                scrap_settings=container_service.website_settings_loader().load_website_settings(
                    website
                )
            ).extract_detail(url=url)
        )
        print(jobdetail.model_dump(mode="json"))
        # Appel au webhook FastAPI
        response = requests.post(
            FASTAPI_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json={
                "task_id": extract_jobdetail.request.id,
                "status": "completed",
                "data": jobdetail.model_dump(mode="json"),
            }
        )

        # Vérifier si l'envoi a réussi
        if response.status_code != 200:
            print(f"Échec d'envoi au webhook: {response.text}")

        return jobdetail.model_dump(mode="json")

    except Exception as e:
        # En cas d'erreur, envoyez également l'information au webhook
        error_result = {
            "task_id": extract_jobdetail.request.id,
            "status": "failed",
            "data": {"error": str(e)},
        }

        try:
            requests.post(
                FASTAPI_WEBHOOK_URL,
                json=error_result,
                headers={"Content-Type": "application/json"},
            )
        except:
            pass  # Ignorer les erreurs lors de la notification d'erreur

        raise
