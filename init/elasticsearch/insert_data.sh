#!/bin/bash

echo ">>> insert_data.sh bien lancé"

ELASTIC_USER="elastic"
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-MasterKeyData45}
ES_URL="http://localhost:9200"
NDJSON_FILE="/emplois.ndjson"

echo "=== DÉMARRAGE INSERTION DONNÉES ==="
echo "Fichier NDJSON: $NDJSON_FILE"
echo "URL Elasticsearch: $ES_URL"
echo "Utilisateur: $ELASTIC_USER"
echo "Mot de passe: $ELASTIC_PASSWORD"

if [ ! -f "$NDJSON_FILE" ]; then
  echo "ERREUR: Fichier $NDJSON_FILE introuvable!"
  ls -la /
  exit 1
fi

echo "Aperçu du fichier NDJSON:"
head -4 "$NDJSON_FILE"

echo "Attente d'Elasticsearch..."
COUNTER=0
until curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/_cluster/health?wait_for_status=yellow&timeout=60s" | grep -q '"status":"yellow"\|"status":"green"'; do
  echo " Attente de l'initialisation d'Elasticsearch... ($COUNTER/12)"
  sleep 5
  COUNTER=$((COUNTER+1))
  if [ $COUNTER -gt 12 ]; then
    echo "ERREUR: Elasticsearch n'est pas disponible après 60 secondes"
    exit 1
  fi
done
echo "Elasticsearch est prêt!"

AUTH_TEST=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/_security/_authenticate")
echo "Test d'authentification: $AUTH_TEST"

echo "Indices existants:"
curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/_cat/indices?v"

INDEX_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/offre_emploi")
echo "Statut de l'index: $INDEX_EXISTS"
if [ "$INDEX_EXISTS" -eq 200 ]; then
  echo "L'index offre_emploi existe déjà, suppression..."
  curl -s -X DELETE "$ES_URL/offre_emploi" -u "$ELASTIC_USER:$ELASTIC_PASSWORD"
  echo "Index supprimé"
fi

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

echo "Insertion des données depuis $NDJSON_FILE..."
BULK_RESULT=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" \
  -H "Content-Type: application/x-ndjson" \
  -XPOST "$ES_URL/_bulk" \
  --data-binary @"$NDJSON_FILE")

echo "$BULK_RESULT" > /bulk_debug.json
cat /bulk_debug.json

if echo "$BULK_RESULT" | grep -q '"errors":false'; then
  echo "Insertion réussie sans erreurs"
else
  echo "Erreurs lors de l'insertion:"
  echo "$BULK_RESULT" | grep -A 5 '"error"'
fi

sleep 2

echo "Vérification du nombre de documents..."
COUNT_RESULT=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/offre_emploi/_count?pretty")
DOC_COUNT=$(echo "$COUNT_RESULT" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ -z "$DOC_COUNT" ]; then
  DOC_COUNT=0
fi
echo "Nombre de documents insérés : $DOC_COUNT"

echo "Vérification du premier document..."
FIRST_DOC=$(curl -s -u "$ELASTIC_USER:$ELASTIC_PASSWORD" "$ES_URL/offre_emploi/_search?size=1&pretty")
echo "$FIRST_DOC"

echo "=== FIN INSERTION DONNÉES ==="

if [ "$DOC_COUNT" -gt 0 ]; then
  echo " SUCCÈS: $DOC_COUNT documents ont été insérés dans l'index offre_emploi"
else
  echo " ÉCHEC: Aucun document n'a été inséré dans l'index offre_emploi"
fi

echo ">>> insert_data.sh terminé"
