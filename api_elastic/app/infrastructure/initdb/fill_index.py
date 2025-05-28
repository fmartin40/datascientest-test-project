from opensearchpy import helpers
from app.core.container import ContainerService


# ingestion d'offres d'emploi fictives
def fill_index():
    jobs = [
        {
            "job_id": "job-1",
            "libelle": "...",
            "date_creation": "2025-05-22",
            "description": "...",
        },
        {
            "job_id": "job-2",
            "libelle": "...",
            "date_creation": "2025-05-22",
            "description": "...",
        },
    ]

    actions = [
        {"_index": "offre_emploi", "_id": job["job_id"], "_source": job} for job in jobs
    ]

    helpers.bulk(ContainerService.opensearch_client(), actions)
