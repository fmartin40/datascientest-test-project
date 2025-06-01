#!/bin/bash

echo ">>> insert_data.sh bien lancé"

ELASTIC_USER="elastic"
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-MasterKeyData45!}
ES_URL="https://search-jobmarketfree-ulvi6zimwplnsg6qmwnjevhx2q.aos.us-east-1.on.aws"
NDJSON_FILE="./bulk_payload.ndjson"

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
