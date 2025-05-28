from app.core.config import settings
from elasticsearch import AsyncElasticsearch


def get_elastic_client():
    try:
        return AsyncElasticsearch(
            hosts=f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}",
            basic_auth=(settings.ELASTIC_USERNAME, settings.ELASTIC_PASSWORD),
        )
    except Exception as e:
        print(f"Erreur de connexion Elasticsearch: {e}")
        raise e
