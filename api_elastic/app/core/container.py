from dependency_injector import containers, providers
from app.infrastructure.sessions.elastic_session import get_es_client
from app.infrastructure.job.job_repository import JobRepositoryElastic


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()
    es_client = providers.Singleton(get_es_client)
    job_repository = providers.Factory(JobRepositoryElastic, es=es_client)
