from elasticsearch import AsyncElasticsearch
from app.core.config import settings


def get_es_client():
    try:
        return AsyncElasticsearch(
            hosts= f"{settings.ELASTIC_HOST}:{settings.ES_PORT}",
            basic_auth=(settings.ELASTIC_USERNAME, settings.ELASTIC_PASSWORD),
        )
    except Exception as e:
        print(e)
        raise e
