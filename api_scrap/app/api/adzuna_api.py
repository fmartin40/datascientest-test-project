import os
import time

import pandas as pd
import requests

from dotenv import load_dotenv
from datetime import datetime

class AdzunaAPI:
  """
  Classe pour interagir avec l'API Adzuna.
  Gère l'authentification, la recherche d'offres et la récupération des détails d'offres.
  """

  COUNTRY= "fr"
  API_URL = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search"

  def __init__(self):
    load_dotenv()
    self.current_date = datetime.now().strftime("%d%m%Y")
    # Récupérer la racine du projet
    self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    # Construire le bon chemin vers `data/`
    self.data_dir = os.path.join(self.root_dir, "data")
    # Vérifier si le dossier `data/` existe, sinon le créer
    if not os.path.exists(self.data_dir):
        os.makedirs(self.data_dir, exist_ok=True)

    self.params = {"app_id": os.getenv("ADZUNA_APP_ID"),
          "app_key": os.getenv("ADZUNA_APP_KEY"),
          "results_per_page" : 20,
          "what" : "data engineer",
          "content-type" : "application/json"}


  def download_page(self, page):
    result = requests.get(f"{self.API_URL}/1", params=self.params)
    if result.status_code == 200:
      print("la page", page, "a été téléchargée avec succès")
      return result.json()['results']
    else:
      print("Le téléchargement a échoué avec le code :", result.status_code)    
      time.sleep(1)
      result = requests.get(f"{self.API_URL}/1", params=self.params)
      if result.status_code == 200:
        return result.json()['results']
      else:
        return []

  def download_all(self):
    all_results = []
    for page in range(1, 11):
      all_results += self.download_page(page)
    return all_results

  def list_to_df(self, results):
    job_list = [{
        "job_id": job.get("id"),
        "title": job.get("title"),
        "company": job.get( "company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "latitude": job.get("latitude"),
        "longitude": job.get("longitude"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "contract_type": job.get("contract_type"),
        "description": job.get("description"),
        "category": job.get("category", {}).get("label"),
        "created": job.get("created"),
        "redirect_url": job.get("redirect_url")
      }
      for job in results]
    
    df = pd.DataFrame(job_list)
    return df

  def df_to_csv(self, df):
    filename = f"{self.current_date}-adzuna-job_data.json"
    filepath = os.path.join(self.data_dir, filename)

    df.to_csv(filepath, index=False)
    print(f"Le fichier Excel a été créé avec succès : {filepath}")

  def main(self):
    results = self.download_all()
    df = self.list_to_df(results)
    self.df_to_csv(df)
