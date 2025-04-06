from dependency_injector import containers, providers
from app.infrastructure.orchestration.celery.server import get_celery_client
from app.core.config import settings

class ContainerService(containers.DeclarativeContainer):
	config = providers.Configuration()
	
	# Configuration de base
	config.from_dict({
		"rabbitmq": {
			"user": settings.RABBITMQ_DEFAULT_USER,
			"password": settings.RABBITMQ_DEFAULT_PASS,
			"url": settings.RABBITMQ_URL,
		},
		"redis": {
			"url": "redis://:1Lau67uh8jPHAkv8IzTRMNzXmNVSALjb@redis-15152.c304.europe-west1-2.gce.cloud.redislabs.com:15152/0"
		}
	})
	
	# Fournir le client Celery comme une ressource
	celery_client = providers.Resource(
		get_celery_client
	)
	
	# Autres services et dépendances
	# ...
	
	# Vous pouvez également créer un Factory Provider pour les tâches Celery
	# celery_task = providers.Factory(
	# 	lambda client, task_name: client.signature(task_name),
	# 	client=celery_client
	# )
