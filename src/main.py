from france_travail_api import FranceTravailAPI

# Exécution principale
if __name__ == "__main__":
    api = FranceTravailAPI()

    api.get_access_token()

    if api.access_token:
        params = {
            "codeROME": "M1805",  # Le code ROME de 'data engineer'
            "motsCles": "data engineer",  
            "sort": "0",     # Tri par pertinence décroissante
            "departement": "75",  # Exemple : Paris (75)
        }

        all_offers  = api.search_offers(params)

        # Afficher le nombre total d'offres
        print(f"Nombre total d'offres trouvées : {len(all_offers)}")
        
        if all_offers:
            api.save_offers_in_json_file(all_offers)
            api.insert_offers_to_db(all_offers)

            # Récupérer les détails pour les 5 premières offres
            for offer in all_offers[:5]:
                offer_id = offer.get('id')
                if offer_id:
                    api.fetch_offer_details(offer_id)
        else:
            print("Aucune offre trouvée.")

    else:
        print("Erreur : impossible de récupérer l'access token.")
