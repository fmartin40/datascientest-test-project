from france_travail_api import FranceTravailAPI
from adzuna_api import AdzunaAPI

if __name__ == "__main__":
    # adzuna_api = AdzunaAPI()
    # adzuna_api.main()

    france_travail_api = FranceTravailAPI()
    france_travail_api.get_access_token()

    if france_travail_api.access_token:
        params = {
            "codeROME": "M1805",  # Le code ROME de 'data engineer'
            "motsCles": "data engineer",  
            "sort": "0",     # Tri par pertinence décroissante
            "departement": "75",  # Exemple : Paris (75)
        }

        all_offers  = france_travail_api.search_offers(params)

    # Afficher le nombre total d'offres
    print(f"Nombre total d'offres trouvées : {len(all_offers)}")

    if all_offers:
        france_travail_api.save_offers_in_json_file(all_offers)
        france_travail_api.insert_offers_to_db(all_offers)

        # Récupérer les détails pour les 5 premières offres
        for offer in all_offers[:5]:
            offer_id = offer.get('id')
            if offer_id:
                france_travail_api.fetch_offer_details(offer_id)
    else:
        print("Aucune offre trouvée.")

else:
    print("Erreur : impossible de récupérer l'access token.")
