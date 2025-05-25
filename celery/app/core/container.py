from dependency_injector import containers, providers
from app.infrastructure.dynamique.load.elastic_loader import ElasticLoader
from app.infrastructure.dynamique.load.postgres_loader import PostgresLoader
from app.infrastructure.dynamique.load.redis_loader import RedisLoader
from app.infrastructure.dynamique.config.webconfig_file import (
    WebsiteSettingsFileLoader,
)
from app.infrastructure.dynamique.scrapers_registry import ScraperRegistry
from app.infrastructure.statique.extract.jobintree import JobInTreeExtractor
from app.infrastructure.statique.transform.competence_transformer import CompetencesTransformer
from app.infrastructure.statique.transform.type_contrat_transformer import TypeContratTransformer   
from app.infrastructure.statique.transform.mode_transformer import ModeTravailTransformer
from app.infrastructure.statique.transform.keyword_transformer import KeywordTransformer


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    
    unstructured_loader = providers.Singleton(ElasticLoader)
    structured_loader = providers.Singleton(PostgresLoader)
    redis_loader = providers.Factory(RedisLoader)

   
    website_settings_loader = providers.Singleton(WebsiteSettingsFileLoader)

    scraper_registry = providers.Singleton(
        ScraperRegistry, config_loader=website_settings_loader
    )
    
    scraper_factory = providers.Dict(
        jobintree=providers.Factory(JobInTreeExtractor)
    )

    competence_transformer = providers.Factory(CompetencesTransformer)
    type_contrat_transformer = providers.Factory(TypeContratTransformer)
    mode_travail_transformer = providers.Factory(ModeTravailTransformer)
    keyword_transformer = providers.Factory(KeywordTransformer)
