from dependency_injector import containers, providers
# from app.infrastructure.orchestration.celery.server import get_celery_client
from app.core.config import settings
from celery import Celery
from app.infrastructure.redis.job_redis import RedisLoader

class ContainerService(containers.DeclarativeContainer):
	config = providers.Configuration()
	
	# Fournir le client Celery comme une ressource
	celery_client = providers.Singleton(
        Celery,
        "jobmarket",
        broker=f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_URL}:5672//",
        backend="rpc://"
    )

	job_repo = providers.Singleton(
        RedisLoader,
    )
	
	
	