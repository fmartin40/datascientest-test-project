from celery import Celery
from app.core.config import settings


broker_url = f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_URL}:5672//"

celery_client = Celery(
    "jobmarket",
    broker=broker_url,
    backend='rpc://'
)

# Configuration Celery
celery_client.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Paris',
    enable_utc=True,
    worker_hijack_root_logger=False,  # Important: ne pas détourner le logger racine
    worker_redirect_stdouts=False,    # Ne pas rediriger stdout/stderr
)
    
# Configuration des limites de rate pour éviter de surcharger les sites
celery_client.conf.task_default_rate_limit = '10/m'  # Limite globale par défaut
