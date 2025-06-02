from dependency_injector import containers, providers
from app.infrastructure.sessions.elastic_session import get_elastic_client
from app.infrastructure.sessions.opensearch_session import get_opensearch_client

from app.infrastructure.elastic.job_reader import JobReaderElastic
from app.infrastructure.elastic.job_writer import JobWriterElastic
from app.infrastructure.opensearch.job_reader import JobReaderOpenSearch
from app.infrastructure.opensearch.job_writer import JobWriterOpenSearch


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Elasticsearch
    elastics_client = providers.Singleton(get_elastic_client)
    job_reader_elastic = providers.Factory(JobReaderElastic, es=elastics_client)
    job_writer_elastic = providers.Factory(JobWriterElastic, es=elastics_client)

    # Opensearch
    opensearch_client = providers.Singleton(get_opensearch_client)
    job_reader_opensearch = providers.Factory(JobReaderOpenSearch, es=opensearch_client)
    job_writer_opensearch = providers.Factory(JobWriterOpenSearch, es=opensearch_client)
