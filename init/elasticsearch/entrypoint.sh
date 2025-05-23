#!/bin/bash
# Lire les mots de passe depuis les variables d'environnement
ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-MasterKeyData45}
KIBANA_PASSWORD=${KIBANA_PASSWORD:-MasterKeyData45}

# Démarrer Elasticsearch en arrière-plan
echo "Démarrage d'Elasticsearch..."
/usr/local/bin/docker-entrypoint.sh elasticsearch &
ES_PID=$!

# Dans Docker, localhost et elasticsearch font référence au même conteneur
# mais assurons-nous de la cohérence
ES_URL="http://localhost:9200"

# Attendre que Elasticsearch soit prêt (vérification active)
echo "Attente de l'initialisation d'Elasticsearch..."
# Essayer de se connecter pendant 2 minutes max
COUNTER=0
until curl -s -u "elastic:${ELASTIC_PASSWORD}" "${ES_URL}/_cluster/health?wait_for_status=yellow" | grep -q '"status":"yellow"\|"status":"green"'; do
    echo "  Elasticsearch n'est pas encore prêt... ($COUNTER/24)"
    sleep 5
    COUNTER=$((COUNTER+1))
    if [ $COUNTER -gt 24 ]; then
      echo "ERREUR: Elasticsearch n'est pas disponible après 120 secondes"
      echo "Dernière tentative de diagnostic:"
      curl -v "http://localhost:9200"
      exit 1
    fi
done
echo "Elasticsearch est prêt !"

# Configuration du mot de passe pour kibana_system directement dans ce script
echo "Configuration du mot de passe pour l'utilisateur kibana_system..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${ES_URL}/_security/user/kibana_system/_password" \
     -H "Content-Type: application/json" \
     -u "elastic:${ELASTIC_PASSWORD}" \
     -d "{\"password\":\"${KIBANA_PASSWORD}\"}")

if [ "$RESPONSE" -eq 200 ]; then
    echo "  Mot de passe kibana_system mis à jour avec succès"
else
    echo "  Échec de mise à jour du mot de passe kibana_system (HTTP $RESPONSE)"
    echo "  Diagnostic:"
    curl -v -u "elastic:${ELASTIC_PASSWORD}" "${ES_URL}/_security/_authenticate"
fi

# Attendre un peu pour être sûr que le mot de passe est bien appliqué
sleep 2

# Vérifier si les scripts existent
echo "Vérification des fichiers d'insertion..."
echo "Contenu de la racine:"
ls -la /
echo "Informations sur insert_data.sh:"
file /insert_data.sh 2>/dev/null || echo "Commande 'file' non disponible ou fichier non trouvé"
echo "Permissions:"
stat /insert_data.sh 2>/dev/null || echo "Commande 'stat' non disponible ou fichier non trouvé"

if [ -f "/insert_data.sh" ]; then
    echo "Script d'insertion trouvé, exécution..."
    echo "Permissions avant chmod:"
    ls -la /insert_data.sh
    chmod +x /insert_data.sh
    echo "Permissions après chmod:"
    ls -la /insert_data.sh
    echo "Exécution du script d'insertion..."
    /insert_data.sh
else
    echo "ERREUR: Script /insert_data.sh non trouvé!"
    echo "Recherche du script dans d'autres emplacements:"
    find / -name "insert_data.sh" 2>/dev/null || echo "Commande 'find' non disponible ou aucun fichier trouvé"
fi

# Vérifier que les données ont été insérées
COUNT=$(curl -s -u "elastic:${ELASTIC_PASSWORD}" "${ES_URL}/offre_emploi/_count" | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ -z "$COUNT" ]; then
    COUNT=0
fi
echo "Nombre de documents insérés : $COUNT"

# Attendre la fin du processus Elasticsearch
echo "Scripts terminés, maintien d'Elasticsearch en exécution..."
wait $ES_PID 