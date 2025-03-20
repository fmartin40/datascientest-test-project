-- Création des tables
CREATE TABLE IF NOT EXISTS "OffreEmploi" ( 
  "id" SERIAL PRIMARY KEY,
  "source" VARCHAR,
  "offre_id" INT,
  "intitule" VARCHAR,
  "description" TEXT,
  "dateCreation" TIMESTAMP,
  "dateActualisation" TIMESTAMP,
  "lieuTravail_id" INT,
  "romeCode" VARCHAR,
  "romeLibelle" VARCHAR,
  "appellationlibelle" VARCHAR,
  "entreprise_id" INT,
  "typeContrat" VARCHAR,
  "typeContratLibelle" VARCHAR,
  "natureContrat" VARCHAR,
  "experienceExige" VARCHAR,
  "experienceLibelle" VARCHAR,
  "experienceCommentaire" VARCHAR
  -- "nombrePostes" INT,
  -- "accessibleTH" BOOLEAN,
  -- "salaire_id" INT,
  -- "contact_id" INT,
  -- "origineOffre_id" INT,
  -- "experience_id" INT,
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

CREATE TABLE IF NOT EXISTS "LieuTravail" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR,
  "latitude" FLOAT,
  "longitude" FLOAT,
  "codePostal" VARCHAR,
  "commune" VARCHAR
);

CREATE TABLE IF NOT EXISTS "Entreprise" (
  "id" SERIAL PRIMARY KEY,
  "nom" VARCHAR,
  "description" VARCHAR,
  "logo" VARCHAR,
  "url" VARCHAR,
  "entrepriseAdaptee" BOOLEAN
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

-- CREATE TABLE IF NOT EXISTS "Contrat" (
--   "id" SERIAL PRIMARY KEY,
--   "typeContrat" VARCHAR,
--   "typeContratLibelle" VARCHAR,
--   "natureContrat" VARCHAR,
--   "alternance"  BOOLEAN
-- );