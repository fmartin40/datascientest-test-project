from dependency_injector import containers, providers
from app.infrastructure.sessions.elastic_session import get_es_client
from app.infrastructure.job.job_reader import JobReader
from app.infrastructure.job.job_writer import JobWriter

class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()
    es_client = providers.Singleton(get_es_client)
    job_reader = providers.Factory(JobReader, es=es_client)
    job_writer = providers.Factory(JobWriter, es=es_client)
