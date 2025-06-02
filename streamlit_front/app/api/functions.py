import requests


def fetch_jobs(params: dict, limit: int = 4):
    try:
        postgres_jobs_url = "http://localhost:8003/jobs"
        elastic_jobs_url = "http://localhost:8002/jobs/ids"
        postgres_jobs_response = requests.get(postgres_jobs_url, params=params)
        postgres_jobs_response.raise_for_status()
        postgres_jobs = postgres_jobs_response.json()

        postgres_jobs = postgres_jobs[:limit]
        job_ids = [job["job_id"] for job in postgres_jobs]
        if not len(job_ids) > 0:
            return postgres_jobs

        elastic_response = requests.get(
            elastic_jobs_url, params={"job_ids": ",".join(job_ids)}
        )
        elastic_response.raise_for_status()
        elastic_jobs = elastic_response.json()

        for postgres_job in postgres_jobs:
            for elastic_job in elastic_jobs:
                if postgres_job["job_id"] == elastic_job["job_id"]:
                    postgres_job["description"] = (
                        f"{elastic_job['description'][:400]}..."
                    )

        return postgres_jobs
    except Exception as e:
        print(e)
        raise


def fetch_skills(ville_id: int):
    try:
        skills_url = "http://localhost:8003/competences/ville"
        response = requests.get(skills_url, params={"ville_id": ville_id})
        response.raise_for_status()
        skills = response.json()
        return skills
    except Exception as e:
        print(e)
        raise


def fetch_timeline_data():
    # À adapter selon l'URL réelle de l'API
    try:
        url = "http://localhost:8003/competences/daily?from_date=2025-04-01&to_date=2025-05-25"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Calcul du total d'offres par jour
        total_by_date = {}
        for item in data:
            for v in item["values"]:
                d = v["date"]
                total_by_date[d] = total_by_date.get(d, 0) + v["count"]
        # Ajout du pourcentage pour chaque compétence/jour
        for item in data:
            for v in item["values"]:
                total = total_by_date.get(v["date"], 0)
                v["pct_offres"] = round(v["count"] / total * 100) if total > 0 else 0.0
        return data
    except Exception as e:
        print(e)
        raise
