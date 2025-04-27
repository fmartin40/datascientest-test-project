from elasticsearch import AsyncElasticsearch
from app.core.config import settings


def get_es_client():
    client = AsyncElasticsearch(
        hosts=f"{settings.ELASTICSEARCH_HOST}:{settings.ES_PORT}",
        http_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD),
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    return client
