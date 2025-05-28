import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

from api.france_travail_api import FranceTravailAPI


# Task 1 - Fetch
def fetch_offers(**kwargs):
    logger = logging.getLogger("airflow.task - Fetch")

    try :
        france_travail_api = FranceTravailAPI()
        france_travail_api.get_access_token()

        if not france_travail_api.access_token:
                logger.error("Token d'accès non récupéré.")
                raise Exception("Token d'accès non récupéré.")
        
        params = {
            "motsCles": "data engineer",  
        }

        all_offers  = france_travail_api.search_offers(params)
        france_travail_api.save_offers_in_json_file(params)

        if not all_offers:
            logger.warning("Aucune offre récupérée avec les paramètres fournis.")
            return  # Ce n’est pas une erreur bloquante

        kwargs['ti'].xcom_push(key='offers', value=all_offers)
        logger.info(f"{len(all_offers)} offres récupérées et envoyées via XCom.")

        logger.info("Task1 terminée avec succès.")
    
    except Exception as e:
        logger.exception(f"Erreur dans fetch_offers : {e}")
        raise  # On relance l'exception pour qu’Airflow marque la tâche comme FAILED


# Task 2 - Save to CSV
def save_offers_to_csv(**kwargs):
    logger = logging.getLogger("airflow.task - Save to CSV")
    
    try :
        france_travail_api = FranceTravailAPI()

        ti = kwargs['ti']
        offers = ti.xcom_pull(task_ids='fetch_data_from_france_travail_api', key='offers')
        
        if not offers:
            logger.warning("Aucune offre reçue pour l'export CSV.")
            return
        
        france_travail_api.save_offers_in_json_file(offers)

        logger.info("Task2 terminée avec succès.")
    
    except Exception as e:
        logger.exception(f"Erreur dans save_offers_to_csv : {e}")
        raise  # On relance l'exception pour qu’Airflow marque la tâche comme FAILED


# Task 3 - Insert in Database
def insert_offers_in_db(**kwargs):
    logger = logging.getLogger("airflow.task - Insert in DB")

    try:
        france_travail_api = FranceTravailAPI()
        ti = kwargs['ti']
        offers = ti.xcom_pull(task_ids='fetch_data_from_france_travail_api', key='offers')

        if not offers:
            logger.warning("Aucune offre reçue pour insertion.")
            return

        france_travail_api.insert_offers_to_db(offers)
        logger.info("Insertion des offres en base terminée avec succès.")

    except Exception as e:
        logger.exception(f"Erreur lors de l'insertion en base : {e}")
        raise
    

# Définition du DAG
with DAG(
    dag_id='france_travail_daily_job_ingestion_dag',
    description='Fetch job postings from France Travail, save in a csv file and insert into PostgreSql',
    tags=['projet', 'datascientest'],
    schedule_interval=None,  # manuel
    start_date=days_ago(2),
    catchup=False,
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
) as dag:
    
    # Task 1: Fetch data from France Travail API
    fetch_data_task = PythonOperator(
        task_id='fetch_data_from_france_travail_api',
        python_callable=fetch_offers,
        provide_context=True,
    )

    save_to_csv_task = PythonOperator(
        task_id='save_offers_to_csv',
        python_callable=save_offers_to_csv,
        provide_context=True,
    )

    insert_offers_task = PythonOperator(
        task_id='insert_offers_in_db',
        python_callable=insert_offers_in_db,
        provide_context=True,
    )

    fetch_data_task >> save_to_csv_task >> insert_offers_task