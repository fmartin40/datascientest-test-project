from dependency_injector import containers, providers
from app.infrastructure.pipelines.load.elastic_loader import ElasticLoader
from app.infrastructure.pipelines.load.postgres_loader import PostgresLoader
from app.infrastructure.pipelines.pipeline_settings.scrap_settings_file_loader import (
    WebsiteSettingsFileLoader,
)
from app.infrastructure.pipelines.scraper_service import ScraperServices
from app.infrastructure.redis.redis_summaries import RedisSummaries
from app.infrastructure.redis.redis_detail import RedisDetail

class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    unstructured_loader = providers.Factory(ElasticLoader)
    structured_loader = providers.Factory(PostgresLoader)
    redis_summaries = providers.Factory(RedisSummaries)
    redis_detail = providers.Factory(RedisDetail)


    website_settings_loader = providers.Factory(WebsiteSettingsFileLoader)

    # Fournit les extractor et transformer en fonction des settings
    # remontés par website_settings_loader pour un site donné
    scrap_services = providers.Factory(ScraperServices)
