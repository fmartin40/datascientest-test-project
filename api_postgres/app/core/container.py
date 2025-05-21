from dependency_injector import containers, providers
from app.infrastructure.job.job_repository import JobRepositoryPostgres


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()
    job_repository = providers.Factory(JobRepositoryPostgres)
