from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
from celery import Celery

# Configuration Celery
celery_app = Celery(
    "jobmarket", broker="amqp://admin:admin@rabbitmq:5672//", backend="rpc://"
)

VILLES = ["paris", "lyon", "marseille"]
METIER = "data engineer"
API_SOURCES = "http://api-postgres:8003/sources"
CELERY_TASK = "statique.extract_summaries"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

with DAG(
    dag_id="scrap_data_engineer_jobs",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["datascientest", "jobmarket"],
) as dag:

    @task
    def get_sources() -> list:
        response = requests.get(API_SOURCES)
        response.raise_for_status()
        sources = response.json()
        return [source["libelle"] for source in sources]

    @task
    def send_scrap_tasks(sites: list):
        for site in sites:
            if site == "jobintree":
                for ville in VILLES:
                    celery_app.send_task(
                        CELERY_TASK,
                        kwargs={"source": site, "query": METIER, "location": ville},
                    )

    # Pipeline
    sites = get_sources()
    send_scrap_tasks(sites)  # type: ignore
