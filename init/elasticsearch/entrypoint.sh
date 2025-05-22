#!/bin/bash

# Lire les mots de passe depuis les variables d'environnement
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-MasterKeyData45}
KIBANA_PASSWORD=${KIBANA_PASSWORD:-MasterKeyData45}

# Démarrer Elasticsearch en arrière-plan
echo "Démarrage d'Elasticsearch..."
/usr/local/bin/docker-entrypoint.sh elasticsearch &
ES_PID=$!

# Attendre que Elasticsearch soit prêt (vérification active)
echo "Attente de l'initialisation d'Elasticsearch..."
until curl -s -u "elastic:${ELASTIC_PASSWORD}" http://localhost:9200/_cluster/health?wait_for_status=yellow | grep -q '"status":"yellow"\|"status":"green"'; do
    echo "  Elasticsearch n'est pas encore prêt..."
    sleep 3
done
echo "Elasticsearch est prêt !"

# Configuration du mot de passe pour kibana_system directement dans ce script
echo "Configuration du mot de passe pour l'utilisateur kibana_system..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:9200/_security/user/kibana_system/_password" \
     -H "Content-Type: application/json" \
     -u "elastic:${ELASTIC_PASSWORD}" \
     -d "{\"password\":\"${KIBANA_PASSWORD}\"}")

if [ "$RESPONSE" -eq 200 ]; then
    echo "  Mot de passe kibana_system mis à jour avec succès"
else
    echo "  Échec de mise à jour du mot de passe kibana_system (HTTP $RESPONSE)"
fi

# Attendre un peu pour être sûr que le mot de passe est bien appliqué
sleep 2

# Exécuter le script d'insertion de données
echo "Exécution du script insert_data.sh..."
/insert_data.sh

# Vérifier que les données ont été insérées
COUNT=$(curl -s -u "elastic:${ELASTIC_PASSWORD}" "http://localhost:9200/offre_emploi/_count" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Nombre de documents insérés : $COUNT"

# Attendre la fin du processus Elasticsearch
echo "Scripts terminés, maintien d'Elasticsearch en exécution..."
wait $ES_PID 