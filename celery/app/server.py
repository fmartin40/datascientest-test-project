from celery import Celery
from app.core.config import settings

broker_url = f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_URL}:5672//"

celery_client = Celery(
    "jobmarket",
    broker=broker_url,
    backend='rpc://'
)