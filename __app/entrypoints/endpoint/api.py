from fastapi import APIRouter, HTTPException, status
from app.domain.common.errors.errors import FetchApiException, NotFoundException
from app.api.france_travail_api import FranceTravailAPI
from app.api.adzuna_api import AdzunaAPI

router = APIRouter(prefix="/api", tags=["API"])
    
@router.post("/process/france_travail/job_offers")
async def process_france_travail_job_offers():

    try: 
        france_travail_api = FranceTravailAPI()
        france_travail_api.get_access_token()

        if france_travail_api.access_token:
            params = {
                "motsCles": "data engineer",  
            }

            all_offers  = france_travail_api.search_offers(params)

            # Afficher le nombre total d'offres
            print(f"Nombre total d'offres trouvées : {len(all_offers)}")
        else:
            print("Erreur de connexion")

        if all_offers:
            france_travail_api.save_offers_in_json_file(all_offers)
            france_travail_api.insert_offers_to_db(all_offers)
        else:
            print("Aucune offre trouvée.")

    except NotFoundException as ne:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ne))
    except FetchApiException as fe:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/process/adzuna/job_offers")
async def process_adzuna_job_offers():

    try: 
        adzuna_api = AdzunaAPI()
        adzuna_api.main()

    except NotFoundException as ne:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ne))
    except FetchApiException as fe:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
