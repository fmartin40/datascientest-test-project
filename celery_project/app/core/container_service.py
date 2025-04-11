from dependency_injector import containers, providers
from app.infrastructure.pipelines.extract.fetchurl import FetchUrl
from app.infrastructure.pipelines.load.elastic_loader import ElasticLoader
from app.infrastructure.pipelines.load.postgres_loader import PostgresLoader
from app.infrastructure.pipelines.pipeline_settings.scrap_settings_file_loader import (
    WebsiteSettingsFileLoader,
)
from app.infrastructure.pipelines.scraper_service import ScraperServices


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    unstructured_loader = providers.Factory(ElasticLoader)
    structured_loader = providers.Factory(PostgresLoader)

    website_settings_loader = providers.Factory(WebsiteSettingsFileLoader)

    # Fournit les extractor et transformer en fonction des settings
    # remontés par website_settings_loader pour un site donné
    scrap_services_provider = providers.Factory(ScraperServices)
