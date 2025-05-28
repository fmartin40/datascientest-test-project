from app.core.config import settings
from opensearchpy import OpenSearch, helpers


def get_opensearch_client():
    try:
        return OpenSearch(
            hosts=[
                {
                    "host": settings.OPENSEARCH_HOST,  # ex: search-xxx.eu-west-3.es.amazonaws.com
                    "port": settings.OPENSEARCH_PORT,
                }
            ],
            http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
            use_ssl=True,
            verify_certs=True,
        )
    except Exception as e:
        print(f"Erreur de connexion OpenSearch: {e}")
        raise e
