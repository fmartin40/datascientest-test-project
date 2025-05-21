-- SOURCES
INSERT INTO "Source" ("libelle") VALUES
('france_travail'),
('jobintree'),
('welcome_to_jungle'),
('glassdoor');

-- ENTREPRISES
INSERT INTO "Entreprise" ("libelle") VALUES
('DataWorks'),
('CloudXpert'),
('AI Builders'),
('NextData');

-- SALAIRES
INSERT INTO "Salaire" ("libelle") VALUES
('35k-45k'),
('45k-55k'),
('55k-65k');

-- FORMATIONS
INSERT INTO "Formation" ("libelle") VALUES
('Master Big Data'),
('Licence Informatique'),
('Certification Cloud');

-- LANGUES
INSERT INTO "Langue" ("libelle") VALUES
('Français'),
('Anglais'),
('Allemand');

-- COMPETENCES
INSERT INTO "Competence" ("libelle") VALUES
('Python'),
('SQL'),
('Spark'),
('Kafka'),
('Airflow');

-- MODES DE TRAVAIL
INSERT INTO "ModeTravail" ("libelle") VALUES
('remote'),
('presentiel'),
('hybride');

-- EXPERIENCES
INSERT INTO "Experience" ("libelle") VALUES
('0-1 an'),
('2-3 ans'),
('3-5 ans'),
('5+ ans');

-- DUREE DE TRAVAIL
INSERT INTO "DureeTravail" ("libelle") VALUES
('Temps plein'),
('Temps partiel');

-- OFFRES D'EMPLOI
INSERT INTO "OffreEmploi" (
  "jobId", "dateCreation", "libelle", "typeContrat",
  "experience_id", "duree_travail_id", "entreprise_id",
  "salaire_id", "mode_travail_id", "source_id"
) VALUES
('a1b2c3d4e5f60718293a4b5c6d7e8f91', NOW(), 'Data Engineer Junior', 'CDI', 1, 1, 1, 1, 1, 1),
('b2c3d4e5f60718293a4b5c6d7e8f91a1', NOW(), 'Data Engineer', 'CDI', 2, 1, 2, 2, 2, 2),
('c3d4e5f60718293a4b5c6d7e8f91a1b2', NOW(), 'Senior Data Engineer', 'CDI', 4, 1, 3, 3, 3, 3),
('d4e5f60718293a4b5c6d7e8f91a1b2c3', NOW(), 'Cloud Data Engineer', 'CDD', 3, 2, 1, 2, 1, 4),
('e5f60718293a4b5c6d7e8f91a1b2c3d4', NOW(), 'ETL Developer', 'CDI', 3, 1, 2, 3, 2, 1),
('f60718293a4b5c6d7e8f91a1b2c3d4e5', NOW(), 'Data Engineer Python', 'CDI', 2, 2, 3, 1, 3, 2),
('0718293a4b5c6d7e8f91a1b2c3d4e5f6', NOW(), 'Big Data Engineer', 'CDI', 3, 1, 1, 2, 1, 3),
('8293a4b5c6d7e8f91a1b2c3d4e5f6071', NOW(), 'Streaming Data Engineer', 'CDI', 2, 1, 2, 3, 2, 4),
('93a4b5c6d7e8f91a1b2c3d4e5f607182', NOW(), 'DataOps Engineer', 'CDI', 3, 1, 3, 1, 3, 1),
('a4b5c6d7e8f91a1b2c3d4e5f60718293', NOW(), 'ML Pipeline Engineer', 'CDI', 2, 1, 1, 2, 2, 2);

-- COMPETENCES PAR OFFRE
INSERT INTO "OffreEmploi_Competence" ("offre_id", "competence_id") VALUES
(1, 1), (1, 2),
(2, 2), (2, 3),
(3, 3), (3, 4),
(4, 4), (4, 5),
(5, 1), (5, 5),
(6, 1), (6, 3),
(7, 2), (7, 4),
(8, 3), (8, 5),
(9, 1), (9, 4),
(10, 2), (10, 5);

-- FORMATIONS PAR OFFRE
INSERT INTO "OffreEmploi_Formation" ("offre_id", "formation_id") VALUES
(1, 1), (2, 2), (3, 3), (4, 1), (5, 2),
(6, 3), (7, 1), (8, 2), (9, 3), (10, 1);

-- LANGUES PAR OFFRE
INSERT INTO "OffreEmploi_Langue" ("offre_id", "langue_id") VALUES
(1, 1), (1, 2),
(2, 2),
(3, 1), (3, 3),
(4, 2),
(5, 3),
(6, 1), (6, 3),
(7, 1),
(8, 2),
(9, 2), (9, 3),
(10, 1), (10, 2);
