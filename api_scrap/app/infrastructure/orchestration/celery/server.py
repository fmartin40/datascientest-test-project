from celery import Celery
from functools import lru_cache
from app.core.config import settings

@lru_cache()
def create_celery_client(broker_url: str, backend_url: str) -> Celery:
    """
    Crée et configure un client Celery.
    Utilise lru_cache pour s'assurer qu'une seule instance est créée.
    """
    client = Celery(
        "jobmarket",
        broker=broker_url,
        backend=backend_url
    )
    
    # Configuration supplémentaire si nécessaire
    client.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Europe/Paris',
        enable_utc=True,
    )
    return client


def get_celery_client():
    """
    Factory function pour obtenir un client Celery configuré.
    Cette fonction sera utilisée par dependency-injector.
    """
    broker_url = f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_URL}:5672//"
    backend_url='rpc://'
    return create_celery_client(broker_url, backend_url)