#!/bin/bash

# Variables avec chemins absolus
ELASTIC_USER="elastic"
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-MasterKeyData45}
ES_URL="http://localhost:9200"
NDJSON_FILE="/emplois.ndjson"

echo "=== DÉMARRAGE INSERTION DONNÉES ==="
echo "Fichier NDJSON: $NDJSON_FILE"
echo "URL Elasticsearch: $ES_URL"

# Vérifier l'existence du fichier NDJSON
if [ ! -f "$NDJSON_FILE" ]; then
  echo "ERREUR: Fichier $NDJSON_FILE introuvable!"
  exit 1
fi

# Attente du démarrage d'Elasticsearch
echo "Attente d'Elasticsearch..."
until curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/_cluster/health?wait_for_status=yellow&timeout=60s" | grep -q '"status":"yellow"\|"status":"green"'; do
  echo " Attente de l'initialisation d'Elasticsearch..."
  sleep 5
done
echo "Elasticsearch est prêt!"

# Création de l'index offre_emploi (avec ignore_exists)
echo "Création de l'index offre_emploi..."
INDEX_RESULT=$(curl -s -X PUT "$ES_URL/offre_emploi?pretty" \
  -H "Content-Type: application/json" \
  -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" \
  -d '{
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    "mappings": {
      "properties": {
        "job_id":        { "type": "keyword" },
        "libelle":       { "type": "text" },
        "date_creation": { "type": "date" },
        "description":   { "type": "text" }
      }
    }
  }')
echo "Résultat création index: $INDEX_RESULT"

# Vérifier que l'index existe
INDEX_CHECK=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/offre_emploi?pretty")
echo "Index check: $INDEX_CHECK"

# Données en format NDJSON
echo "Insertion des données depuis $NDJSON_FILE..."
BULK_RESULT=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" \
  -H "Content-Type: application/x-ndjson" \
  -XPOST "$ES_URL/_bulk" \
  --data-binary @"$NDJSON_FILE")
echo "Résultat insertion: $BULK_RESULT"

# Vérifier que les documents ont été insérés
COUNT_RESULT=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/offre_emploi/_count?pretty")
echo "Nombre de documents: $COUNT_RESULT"

echo "=== FIN INSERTION DONNÉES ==="