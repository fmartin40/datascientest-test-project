#!/bin/bash

#!/bin/bash

# On attend que Elasticsearch soit prêt et que la sécurité soit active
until curl -s -u "elastic:MasterKeyData45" http://localhost:9200/_security/_authenticate  | grep -q '"username"' ; do
    echo " Waiting for Elasticsearch security to be ready..."
    sleep 2
done

# On crée ou réinitialise le mot de passe du compte kibana_system
echo " Création ou mise à jour du mot de passe de 'kibana_system'"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:9200/_security/user/kibana_system/_password" \
     -H "Content-Type: application/json" \
     -u "elastic:MasterKeyData45" \
     -d "{\"password\":\"MasterKeyData45\"}")

if [ "$RESPONSE" -eq 200 ]; then
    echo " Mot de passe kibana_system mis à jour"
else
    echo " Échec de mise à jour du mot de passe kibana_system (HTTP $RESPONSE)"
fi

