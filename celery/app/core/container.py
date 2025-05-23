from dependency_injector import containers, providers
from app.infrastructure.dynamique.load.elastic_loader import ElasticLoader
from app.infrastructure.dynamique.load.postgres_loader import PostgresLoader
from app.infrastructure.dynamique.load.redis_loader import RedisLoader
from app.infrastructure.dynamique.config.webconfig_file import (
    WebsiteSettingsFileLoader,
)
from app.infrastructure.dynamique.scrapers_registry import ScraperRegistry
from app.infrastructure.statique.scraper import Scraper

class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    unstructured_loader = providers.Singleton(ElasticLoader)
    structured_loader = providers.Singleton(PostgresLoader)
    redis_loader = providers.Factory(RedisLoader)

    website_settings_loader = providers.Singleton(WebsiteSettingsFileLoader)

    scraper_registry = providers.Singleton(
        ScraperRegistry, config_loader=website_settings_loader
    )
    
    static_scrapers = providers.Dict(
        jobintree=providers.Factory(Scraper, source="jobintree")
    )
