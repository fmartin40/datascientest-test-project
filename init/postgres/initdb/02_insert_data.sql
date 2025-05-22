-- =======================
-- Données de référence
-- =======================

-- Langues
INSERT INTO "Langue" (libelle) VALUES 
('fr'), ('de'), ('en');

-- Compétences
INSERT INTO "Competence" (libelle) VALUES 
('Docker'), ('Kubernetes'), ('Spark'), ('SQL'), ('Airflow'), 
('Kafka'), ('Hadoop'), ('Scala'), ('Pandas'), ('MongoDB');

-- Entreprises (utilisées comme villes)
INSERT INTO "Entreprise" (libelle) VALUES 
('Xebia'), ('Capgemini'), ('Atos');

-- Villes
INSERT INTO "Ville" (libelle) VALUES 
('Paris'), ('Lyon'), ('Marseille');

-- Sources
INSERT INTO "Source" (libelle) VALUES 
('jobintree'), ('muse'), ('emploi_informatique'), ('option_carriere');

-- Types de contrat
INSERT INTO "TypeContrat" (libelle) VALUES 
('CDD'), ('CDI'), ('alternance');

-- Modes de travail
INSERT INTO "ModeTravail" (libelle) VALUES 
('télétravail'), ('présentiel'), ('hybride');

-- Durées de travail
INSERT INTO "DureeTravail" (libelle) VALUES 
('temps plein'), ('temps partiel');

-- Salaires
INSERT INTO "Salaire" (libelle) VALUES 
('40k-50k'), ('50k-60k'), ('60k-70k');

-- Formations
INSERT INTO "Formation" (libelle) VALUES 
('Licence Informatique'), ('Master Data'), ('Bootcamp Big Data');

-- Expériences
INSERT INTO "Experience" (libelle) VALUES 
('3 ans');

-- =======================
-- Offres d'emploi (titres variés)
-- =======================

INSERT INTO "OffreEmploi" (
    "jobId", "dateCreation", "libelle",
    "experience_id", "duree_travail_id", "entreprise_id",
    "salaire_id", "mode_travail_id", "type_contrat_id", "source_id","ville_id"
) VALUES 
('job-1', CURRENT_DATE, 'Ingénieur Data – Spécialiste Pipeline & Big Data', 1, 1, 1, 1, 1, 1, 1, 1),
('job-2', CURRENT_DATE, 'Développeur Data – ETL & Traitement Distribué', 1, 2, 3, 2, 3, 2, 4, 2),
('job-3', CURRENT_DATE, 'Architecte Données – Infrastructure Cloud & On-Prem', 1, 1, 2, 3, 2, 3, 3, 2),
('job-4', CURRENT_DATE, 'Data Engineer Python – Stack Open Source', 1, 2, 1, 2, 2, 2, 2, 3),
('job-5', CURRENT_DATE, 'Spécialiste Data Pipeline – Projet Retail Analytics', 1, 1, 3, 1, 1, 3, 1, 3),
('job-6', CURRENT_DATE, 'Ingénieur Données – Temps Réel & Kafka', 1, 2, 2, 3, 3, 2, 3, 1),
('job-7', CURRENT_DATE, 'Consultant Data Engineering – Cloud AWS', 1, 1, 1, 1, 1, 1, 4, 1),
('job-8', CURRENT_DATE, 'Data Engineer Confirmé – Projets IoT & Smart City', 1, 2, 3, 2, 2, 2, 1, 2),
('job-9', CURRENT_DATE, 'Expert Pipeline Données – Machine Learning Ready', 1, 1, 2, 3, 3, 3, 2, 3),
('job-10', CURRENT_DATE, 'Développeur Data – Monitoring et Observabilité', 1, 2, 1, 2, 1, 2, 3, 1);

-- =======================
-- Relations Offre ↔ Formation
-- =======================

INSERT INTO "OffreEmploi_Formation" (offre_id, formation_id) VALUES 
(1, 1), (2, 2), (3, 3), (4, 1), (5, 2), 
(6, 3), (7, 1), (8, 2), (9, 3), (10, 1);

-- =======================
-- Relations Offre ↔ Langue
-- =======================

INSERT INTO "OffreEmploi_Langue" (offre_id, langue_id) VALUES 
(1, 1), (2, 2), (3, 3), (4, 1), (5, 2), 
(6, 3), (7, 1), (8, 2), (9, 3), (10, 1);

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
