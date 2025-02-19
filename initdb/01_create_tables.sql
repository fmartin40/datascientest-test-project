-- Création des tables
CREATE TABLE IF NOT EXISTS "OffreEmploi" ( 
  "id" SERIAL PRIMARY KEY,
  "source" VARCHAR,
  "id_Source" INT,
  "intitule" VARCHAR,
  "description" TEXT,
  "dateCreation" TIMESTAMP,
  -- "dateActualisation" TIMESTAMP,
  -- "nombrePostes" INT,
  -- "accessibleTH" BOOLEAN,
  -- "lieuTravail_id" INT,
  -- "entreprise_id" INT,
  -- "salaire_id" INT,
  -- "contact_id" INT,
  -- "origineOffre_id" INT,
  -- "rome_id" INT,
  -- "experience_id" INT,
  "contrat_id" INT
  -- "agence_id" INT,
  -- "deplacement_id" INT,
  -- "qualification_id" INT,
  -- "dureeTravailLibelle" VARCHAR,
  -- "dureeTravailLibelleConverti" VARCHAR,
  -- "complementExercice" VARCHAR,
  -- "conditionExercice" VARCHAR,
  -- "secteurActivite" VARCHAR,
  -- "secteurActiviteLibelle" VARCHAR,
  -- "trancheEffectifEtab" VARCHAR,
  -- "offresManqueCandidats" BOOLEAN
);

-- CREATE TABLE IF NOT EXISTS "Deplacement" (
--   "id" SERIAL PRIMARY KEY,
--   "code" VARCHAR,
--   "libelle" VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS "Qualification" (
--   "id" SERIAL PRIMARY KEY,
--   "code" VARCHAR,
--   "libelle" VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS "Agence" (
--   "id" SERIAL PRIMARY KEY,
--   "telephone" VARCHAR,
--   "courriel" VARCHAR
-- );

CREATE TABLE IF NOT EXISTS "Contrat" (
  "id" SERIAL PRIMARY KEY,
  "typeContrat" VARCHAR,
  "typeContratLibelle" VARCHAR,
  "natureContrat" VARCHAR,
  "alternance"  BOOLEAN
);