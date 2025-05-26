-- =======================
-- Données de référence
-- =======================



-- Compétences
INSERT INTO "Competence" (libelle) VALUES
-- Langages
('python'),
('java'),
('scala'),
('sql'),
('bash'),
('go'),
('shell'),

-- Libs & Frameworks
('pandas'),
('numpy'),
('pyarrow'),
('polars'),
('fastapi'),

-- Orchestration & ETL
('airflow'),
('luigi'),
('dagster'),
('prefect'),
('dbt'),
('talend'),
('nifi'),
('informatica'),
('matillion'),
('stitch'),
('fivetran'),

-- Cloud & stockage
('aws'),
('gcp'),
('azure'),
('s3'),
('gcs'),
('bigquery'),
('redshift'),
('snowflake'),
('databricks'),
('synapse'),
('data lake'),
('data warehouse'),

-- Bases de données SQL
('postgresql'),
('mysql'),
('sql server'),
('clickhouse'),

-- Bases de données NoSQL
('mongodb'),
('cassandra'),
('dynamodb'),
('redis'),
('elasticsearch'),
('neo4j'),

-- Streaming / batch
('kafka'),
('kinesis'),
('flink'),
('spark'),
('beam'),
('hadoop'),

-- CI / CD / DevOps
('git'),
('github'),
('gitlab'),
('ci/cd'),
('jenkins'),
('github actions'),
('gitlab ci/cd'),
('terraform'),
('ansible'),
('vault'),
('docker'),
('kubernetes'),
('helm'),

-- Monitoring & observability
('grafana'),
('prometheus'),
('datadog'),

-- Sécurité & gestion d’accès
('iam'),
('oauth2'),

-- Autres
('superset'),
('looker'),
('tableau'),
('powerbi'),
('soda'),
('great expectations')
ON CONFLICT (libelle) DO NOTHING;




-- Entreprises
INSERT INTO "Entreprise" (libelle) VALUES 
('Xebia'), ('Capgemini'), ('Atos');

-- Villes
INSERT INTO "Ville" (libelle) VALUES 
('nc'), ('paris'), ('lyon'), ('marseille');

-- Sources
INSERT INTO "Source" (libelle) VALUES 
('jobintree'), ('muse'), ('emploi_informatique'), ('option_carriere');

-- Types de contrat
INSERT INTO "TypeContrat" (libelle) VALUES 
('CDI'), ('CDD'), ('alternance'), ('indépendant');

-- Modes de travail
INSERT INTO "ModeTravail" (libelle) VALUES 
('présentiel'), ('télétravail'), ('hybride');

-- Durées de travail
INSERT INTO "DureeTravail" (libelle) VALUES 
('temps plein'), ('temps partiel');

-- =======================
-- Offres d'emploi (titres variés)
-- =======================

INSERT INTO "OffreEmploi" (
    "jobId", "url", "dateCreation", "libelle",
    "duree_travail_id", "entreprise_id",
    "mode_travail_id", "type_contrat_id", "source_id", "ville_id"
) VALUES 
('job-1', 'https://www.jobintree.com/offre-emploi/ingenieur-data-specialiste-pipeline-big-data', CURRENT_DATE, 'Ingénieur Data – Spécialiste Pipeline & Big Data', 1, 1, 1, 1, 1, 1),
('job-2', 'https://www.jobintree.com/offre-emploi/developpeur-data-etl-traitement-distribue', CURRENT_DATE, 'Développeur Data – ETL & Traitement Distribué', 2, 3, 3, 2, 4, 2),
('job-3', 'https://www.jobintree.com/offre-emploi/architecte-donnees-infrastructure-cloud-on-prem', CURRENT_DATE, 'Architecte Données – Infrastructure Cloud & On-Prem', 1, 2, 2, 3, 3, 2),
('job-4', 'https://www.jobintree.com/offre-emploi/data-engineer-python-stack-open-source', CURRENT_DATE, 'Data Engineer Python – Stack Open Source', 2, 1, 2, 2, 2, 3),
('job-5', 'https://www.jobintree.com/offre-emploi/specialiste-data-pipeline-projet-retail-analytics', CURRENT_DATE, 'Spécialiste Data Pipeline – Projet Retail Analytics', 1, 3, 1, 3, 1, 3),
('job-6', 'https://www.jobintree.com/offre-emploi/ingenieur-donnees-temps-reel-kafka', CURRENT_DATE, 'Ingénieur Données – Temps Réel & Kafka', 2, 2, 3, 2, 3, 1),
('job-7', 'https://www.jobintree.com/offre-emploi/consultant-data-engineering-cloud-aws', CURRENT_DATE, 'Consultant Data Engineering – Cloud AWS', 1, 1, 1, 1, 4, 1),
('job-8', 'https://www.jobintree.com/offre-emploi/data-engineer-confirmé-projets-iot-smart-city', CURRENT_DATE, 'Data Engineer Confirmé – Projets IoT & Smart City', 2, 3, 2, 2, 1, 2),
('job-9', 'https://www.jobintree.com/offre-emploi/expert-pipeline-donnees-machine-learning-ready', CURRENT_DATE, 'Expert Pipeline Données – Machine Learning Ready', 1, 2, 3, 3, 2, 3),
('job-10', 'https://www.jobintree.com/offre-emploi/developpeur-data-monitoring-observabilite', CURRENT_DATE, 'Développeur Data – Monitoring et Observabilité', 2, 1, 1, 2, 3, 1);



-- =======================
-- Relations Offre ↔ Compétences
-- =======================

INSERT INTO "OffreEmploi_Competence" (offre_id, competence_id) VALUES 
(1,1), (1,2), (1,3),
(2,4), (2,5), (2,6),
(3,7), (3,8), (3,9),
(4,10), (4,1), (4,2),
(5,3), (5,4), (5,5),
(6,6), (6,7), (6,8),
(7,9), (7,10), (7,1),
(8,2), (8,3), (8,4),
(9,5), (9,6), (9,7),
(10,8), (10,9), (10,10);

-- =======================
-- Relations Offre ↔ Type de contrat
-- =======================

INSERT INTO "MappingTypeContrat" (libelle, type_contrat_id)

-- CDI (Contrat à durée indéterminée)
SELECT 'CDI', id FROM "TypeContrat" WHERE libelle = 'CDI'
UNION ALL SELECT 'contrat à durée indéterminée', id FROM "TypeContrat" WHERE libelle = 'CDI'
UNION ALL SELECT 'contrat durée indéterminée', id FROM "TypeContrat" WHERE libelle = 'CDI'
UNION ALL SELECT 'permanent contract', id FROM "TypeContrat" WHERE libelle = 'CDI'
UNION ALL SELECT 'full-time permanent', id FROM "TypeContrat" WHERE libelle = 'CDI'
UNION ALL SELECT 'permanent', id FROM "TypeContrat" WHERE libelle = 'CDI'

-- CDD (Contrat à durée déterminée)
UNION ALL SELECT 'CDD', id FROM "TypeContrat" WHERE libelle = 'CDD'
UNION ALL SELECT 'contrat à durée déterminée', id FROM "TypeContrat" WHERE libelle = 'CDD'
UNION ALL SELECT 'contrat durée déterminée', id FROM "TypeContrat" WHERE libelle = 'CDD'
UNION ALL SELECT 'fixed-term contract', id FROM "TypeContrat" WHERE libelle = 'CDD'
UNION ALL SELECT 'short-term contract', id FROM "TypeContrat" WHERE libelle = 'CDD'
UNION ALL SELECT 'contractuel', id FROM "TypeContrat" WHERE libelle = 'CDD'

-- Alternance
UNION ALL SELECT 'alternance', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'contrat en alternance', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'contrat alternance', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'apprentissage', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'contrat apprentissage', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'contrat d''apprentissage', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'stage', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'internship', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'trainee', id FROM "TypeContrat" WHERE libelle = 'alternance'
UNION ALL SELECT 'intern', id FROM "TypeContrat" WHERE libelle = 'alternance'
ON CONFLICT (libelle) DO NOTHING;

-- Indépendant
UNION ALL SELECT 'indépendant', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'freelance', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'auto-entrepreneur', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'micro-entrepreneur', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'independant', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'consultant indépendant', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'travailleur indépendant', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'independent worker', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'freelancer', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'contractor', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'portage salarial', id FROM "TypeContrat" WHERE libelle = 'indépendant'
UNION ALL SELECT 'portage', id FROM "TypeContrat" WHERE libelle = 'indépendant'
ON CONFLICT (libelle) DO NOTHING;

-- =======================
-- Relations Offre ↔ Mode de travail
-- =======================

INSERT INTO "MappingModeTravail" (libelle, mode_travail_id)

-- Présentiel
SELECT 'présentiel', id FROM "ModeTravail" WHERE libelle = 'présentiel'
UNION ALL SELECT 'presentiel', id FROM "ModeTravail" WHERE libelle = 'présentiel'
UNION ALL SELECT 'sur site', id FROM "ModeTravail" WHERE libelle = 'présentiel'
UNION ALL SELECT 'on-site', id FROM "ModeTravail" WHERE libelle = 'présentiel'
UNION ALL SELECT 'work on site', id FROM "ModeTravail" WHERE libelle = 'présentiel'
UNION ALL SELECT 'workplace', id FROM "ModeTravail" WHERE libelle = 'présentiel'

-- Télétravail
UNION ALL SELECT 'télétravail', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'teletravail', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'remote', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'remote only', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'remote work', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'full remote', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'travail à distance', id FROM "ModeTravail" WHERE libelle = 'télétravail'
UNION ALL SELECT 'travail 100% à distance', id FROM "ModeTravail" WHERE libelle = 'télétravail'

-- Hybride
UNION ALL SELECT 'hybride', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'hybrid', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'part remote', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'partial remote', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'remote / on-site', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'remote and on-site', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'télétravail partiel', id FROM "ModeTravail" WHERE libelle = 'hybride'
UNION ALL SELECT 'travail hybride', id FROM "ModeTravail" WHERE libelle = 'hybride'
ON CONFLICT (libelle) DO NOTHING;

-- =======================
-- Relations Offre ↔ Durée de travail
-- =======================

INSERT INTO "MappingDureeTravail" (libelle, duree_travail_id)

-- Temps plein
SELECT 'temps plein', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'temps complet', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'plein temps', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'travail à temps plein', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'travail temps plein', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'poste temps plein', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'full time', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'full-time', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'fulltime', id FROM "DureeTravail" WHERE libelle = 'temps plein'
UNION ALL SELECT 'full-time position', id FROM "DureeTravail" WHERE libelle = 'temps plein'

-- Temps partiel
UNION ALL SELECT 'temps partiel', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'mi-temps', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'travail à temps partiel', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'poste temps partiel', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'travail partiel', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'part time', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'part-time', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'parttime', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
UNION ALL SELECT 'part-time position', id FROM "DureeTravail" WHERE libelle = 'temps partiel'
ON CONFLICT (libelle) DO NOTHING;

-- =======================
-- Relations Offre ↔ Compétence (mots-clés synonymes)
-- =======================

INSERT INTO "MappingCompetence" (libelle, competence_id)

-- Python
SELECT 'python3', id FROM "Competence" WHERE libelle = 'python'
UNION ALL SELECT 'py', id FROM "Competence" WHERE libelle = 'python'

-- PostgreSQL
UNION ALL SELECT 'postgres', id FROM "Competence" WHERE libelle = 'postgresql'
UNION ALL SELECT 'postgresql database', id FROM "Competence" WHERE libelle = 'postgresql'

-- MySQL
UNION ALL SELECT 'oracle mysql', id FROM "Competence" WHERE libelle = 'mysql'
UNION ALL SELECT 'mariadb', id FROM "Competence" WHERE libelle = 'mysql'

-- AWS
UNION ALL SELECT 'amazon web services', id FROM "Competence" WHERE libelle = 'aws'

-- GCP
UNION ALL SELECT 'google cloud platform', id FROM "Competence" WHERE libelle = 'gcp'
UNION ALL SELECT 'google cloud', id FROM "Competence" WHERE libelle = 'gcp'

-- GCS
UNION ALL SELECT 'google cloud storage', id FROM "Competence" WHERE libelle = 'gcs'

-- Spark
UNION ALL SELECT 'apache spark', id FROM "Competence" WHERE libelle = 'spark'

-- Airflow
UNION ALL SELECT 'apache airflow', id FROM "Competence" WHERE libelle = 'airflow'

-- Beam
UNION ALL SELECT 'apache beam', id FROM "Competence" WHERE libelle = 'beam'

-- Redis
UNION ALL SELECT 'redis db', id FROM "Competence" WHERE libelle = 'redis'

-- CI/CD
UNION ALL SELECT 'continuous integration', id FROM "Competence" WHERE libelle = 'ci/cd'
UNION ALL SELECT 'continuous delivery', id FROM "Competence" WHERE libelle = 'ci/cd'

-- Terraform
UNION ALL SELECT 'iac', id FROM "Competence" WHERE libelle = 'terraform'

-- Snowflake
UNION ALL SELECT 'sf', id FROM "Competence" WHERE libelle = 'snowflake'

-- Looker
UNION ALL SELECT 'looker studio', id FROM "Competence" WHERE libelle = 'looker'

-- Superset
UNION ALL SELECT 'apache superset', id FROM "Competence" WHERE libelle = 'superset'

-- GitLab CI
UNION ALL SELECT 'gitlab pipeline', id FROM "Competence" WHERE libelle = 'gitlab ci/cd'

-- GitHub Actions
UNION ALL SELECT 'gh actions', id FROM "Competence" WHERE libelle = 'github actions'

-- Jenkins
UNION ALL SELECT 'jenkins pipeline', id FROM "Competence" WHERE libelle = 'jenkins'

-- MongoDB
UNION ALL SELECT 'mongo', id FROM "Competence" WHERE libelle = 'mongodb'

-- Kubernetes
UNION ALL SELECT 'k8s', id FROM "Competence" WHERE libelle = 'kubernetes'

-- Docker
UNION ALL SELECT 'containerisation', id FROM "Competence" WHERE libelle = 'docker'

-- DBT
UNION ALL SELECT 'data build tool', id FROM "Competence" WHERE libelle = 'dbt'

-- PowerBI
UNION ALL SELECT 'power bi', id FROM "Competence" WHERE libelle = 'powerbi'

ON CONFLICT (libelle) DO NOTHING;
