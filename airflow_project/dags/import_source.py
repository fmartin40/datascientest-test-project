from decorators import dag, task
from utils.dates import days_ago
import requests
import logging


@task
def fetch_sources():
    url = "http://localhost:8003/sources"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        libelles = [item["libelle"] for item in data if "libelle" in item]
        logging.info(f"Libellés récupérés : {libelles}")
        return libelles
    except Exception as e:
        logging.error(f"Erreur API : {e}")
        raise


@task
def print_libelles(libelles):
    print("Libellés extraits :")
    for libelle in libelles:
        print(f" - {libelle}")


@dag(
    dag_id="job_market_import_sources",
    tags=["job_market", "postgres", "jobs"],
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
)
def dag_main():
    result = fetch_sources()
    print_libelles(result)


dag_instance = dag_main()
