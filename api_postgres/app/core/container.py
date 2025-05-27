from dependency_injector import containers, providers
from app.infrastructure.job.job_reader import JobReader
from app.infrastructure.job.job_writer import JobWriter
from app.infrastructure.job.mappings import Mappings
from app.infrastructure.stats.stats_reader import StatsReader


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()
    job_reader = providers.Factory(JobReader)
    job_writer = providers.Factory(JobWriter)
    mappings = providers.Factory(Mappings)
    stats_reader = providers.Factory(StatsReader)
