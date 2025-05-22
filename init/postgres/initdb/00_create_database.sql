-- Vérifie si la base de données "job_market" existe déjà
SELECT 'CREATE DATABASE job_market'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'job_market')
\gexec