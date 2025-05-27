-- Vérifie si la base de données "job_market" existe déjà
SELECT 'CREATE DATABASE job_market'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'job_market')
\gexec

-- Vérifie si la base de données "airflow" existe déjà
SELECT 'CREATE DATABASE airflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')
\gexec