import requests
import json
import os

from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les variables d'environnement
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# URL pour générer l'access token
ACCESS_TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"

# URL pour l'api France Travail
SEARCH_API_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
OFFER_API_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/{id}"

data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'api_offresdemploiv2 o2dsoffre'
}

session = requests.Session()
session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

current_date = datetime.now().strftime("%d%m%Y")

def get_access_token():
    try:
        response = session.post(ACCESS_TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du token : {e}")
        return None

def search_offers(access_token, params):
    headers = {'Authorization': f'Bearer {access_token}'}
    all_offers = []
    range_start = 0 
    range_step = 50

    while True:
        # Définition le paramètre de pagination "range" pour cette requête
        params['range'] = f"{range_start}-{range_start + range_step - 1}"

        try:
            response = requests.get(SEARCH_API_URL, headers=headers, params=params)
            if response.status_code == 200:
                # Toutes les annonces ont été envoyées en une seule fois
                data = response.json()
                all_offers.extend(data.get('resultats', []))
                print("Toutes les offres ont été récupérées en une seule fois.")
                break
            elif response.status_code == 206:
                # Réponse partielle : récupération des annonces de cette page
                data = response.json()
                offers = data.get('resultats', [])
                print(f"Nombre d'offres reçues lors de cet appel : {len(offers)}")
                all_offers.extend(offers)

                # Condition de fin : si moins de 50 offres sont reçues, fin de pagination
                if len(offers) < range_step:
                    print("Fin de la pagination : toutes les offres ont été récupérées.")
                    break
                else:
                    # Continuer la pagination si on reçoit exactement `range_step` offres
                    range_start += range_step
            elif response.status_code == 204:
                print("Aucune offre ne correspond aux critères de recherche.")
                break
            elif response.status_code == 400:
                print("Erreur 400 : Requête invalide. Vérifiez les paramètres.")
                break
            elif response.status_code == 500:
                print("Erreur 500 : Erreur interne du serveur. Réessayez plus tard.")
                break
            else:
                print(f"Code de réponse inattendu : {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des offres : {e}")
            break

    return all_offers

def fetch_offer_details(access_token, offer_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = OFFER_API_URL.format(id=offer_id)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Sauvegarde des détails de l'offre dans un fichier JSON
        offer_details = response.json()

        filename = f"{current_date}-{offer_id}.json"
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(offer_details, f, ensure_ascii=False, indent=4)
        print(f"Détails de l'offre {offer_id} sauvegardés dans {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des détails de l'offre {offer_id} : {e}")

access_token = get_access_token()

if access_token:
    params = {
    # "codeROME": "M1805",  # Le code ROME de 'data engineer'
    "motsCles": "data engineer",  
    "sort": "0",     # Tri par pertinence décroissante
    "departement": "75",  # Exemple : Paris (75)
    }

    all_offers  = search_offers(access_token, params)

    # Afficher le nombre total d'offres
    print(f"Nombre total d'offres reçues : {len(all_offers)}")
    
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    filename = f"{current_date}-offres_d_emploi.json"
    filepath = os.path.join(data_dir, filename)

    print(filepath)

    if all_offers:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_offers, f, ensure_ascii=False, indent=4)
        
        # Récupérer les détails pour les 5 premières offres
        for offer in all_offers[:5]:
            offer_id = offer.get('id')
            if offer_id:
                fetch_offer_details(access_token, offer_id)
    else:
        print("Aucune offre trouvée.")

else:
    print("Erreur : impossible de récupérer l'access token.")