from dependency_injector import containers, providers

# from app.workers.infrastructure.dynamique.config.webconfig_file import (
#     WebsiteSettingsFileLoader,
# )
# from app.workers.infrastructure.dynamique.scrapers_registry import ScraperRegistry

from app.workers.infrastructure.statique.load.elastic_loader import ElasticLoader
from app.workers.infrastructure.statique.load.postgres_loader import PostgresLoader
from app.workers.infrastructure.statique.load.redis_loader import RedisLoader
from app.workers.infrastructure.statique.extract.jobintree import JobInTreeExtractor
# from app.workers.infrastructure.statique.transform.competence_transformer import (
#     CompetencesTransformer,
# )
# from app.workers.infrastructure.statique.transform.type_contrat_transformer import (
#     TypeContratTransformer,
# )
# from app.workers.infrastructure.statique.transform.mode_transformer import (
#     ModeTravailTransformer,
# )
# from app.workers.infrastructure.statique.transform.mapping_transformer import (
#     MappingTransformer,
# )
from app.workers.infrastructure.statique.load.mapping_loader import MappingsFromPostgres


class ContainerService(containers.DeclarativeContainer):
    config = providers.Configuration()

    unstructured_loader = providers.Singleton(ElasticLoader)
    structured_loader = providers.Singleton(PostgresLoader)
    redis_loader = providers.Factory(RedisLoader)

    # website_settings_loader = providers.Singleton(WebsiteSettingsFileLoader)

    # scraper_registry = providers.Singleton(
    #     ScraperRegistry, config_loader=website_settings_loader
    # )

    mappings_loader = providers.Factory(MappingsFromPostgres)

    # competence_transformer = providers.Factory(CompetencesTransformer)
    # type_contrat_transformer = providers.Factory(TypeContratTransformer)
    # mode_travail_transformer = providers.Factory(ModeTravailTransformer)
    # mapping_transformer = providers.Factory(MappingTransformer, mapping=mappings_loader)
    

    scraper_factory = providers.Dict(
        jobintree=providers.Factory(
            JobInTreeExtractor,
            keywords_loader=mappings_loader
        )
    )
