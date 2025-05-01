from dependency_injector import containers, providers
from app.infrastructure.scrap.load.elastic_loader import ElasticLoader
from app.infrastructure.scrap.load.postgres_loader import PostgresLoader
from app.infrastructure.scrap.load.redis_loader import RedisLoader
from app.infrastructure.scrap.config.webconfig_file import (
    WebsiteSettingsFileLoader,
)
from app.infrastructure.scrap.scrapers_registry import ScraperRegistry


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    unstructured_loader = providers.Singleton(ElasticLoader)
    structured_loader = providers.Singleton(PostgresLoader)
    redis_loader = providers.Factory(RedisLoader)

    website_settings_loader = providers.Singleton(WebsiteSettingsFileLoader)

    scraper_registry = providers.Singleton(
        ScraperRegistry, config_loader=website_settings_loader
    )
