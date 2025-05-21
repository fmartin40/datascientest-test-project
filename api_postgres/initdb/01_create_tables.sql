-- TABLES DE RÉFÉRENCE
CREATE TABLE IF NOT EXISTS "Entreprise" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "Salaire" (
  "id" SERIAL PRIMARY KEY,
  "libelle" TEXT
);

CREATE TABLE IF NOT EXISTS "Formation" (
  "id" SERIAL PRIMARY KEY,
  "libelle" TEXT
);

CREATE TABLE IF NOT EXISTS "Langue" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS "Competence" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "Experience" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "DureeTravail" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "ModeTravail" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS "Source" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

-- TABLE PRINCIPALE
CREATE TABLE IF NOT EXISTS "OffreEmploi" (
  "id" SERIAL PRIMARY KEY,
  "jobId" VARCHAR(255),
  "dateCreation" TIMESTAMP,
  "libelle" VARCHAR(255),
  "typeContrat" VARCHAR(255),
  "experience_id" INT REFERENCES "Experience"("id") ON DELETE SET NULL,
  "duree_travail_id" INT REFERENCES "DureeTravail"("id") ON DELETE SET NULL,
  "entreprise_id" INT REFERENCES "Entreprise"("id") ON DELETE SET NULL,
  "salaire_id" INT REFERENCES "Salaire"("id") ON DELETE SET NULL,
  "mode_travail_id" INT REFERENCES "ModeTravail"("id") ON DELETE SET NULL,
  "source_id" INT REFERENCES "Source"("id") ON DELETE SET NULL
);

-- RELATIONS N:N
CREATE TABLE IF NOT EXISTS "OffreEmploi_Formation" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "formation_id" INT REFERENCES "Formation"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "formation_id")
);

CREATE TABLE IF NOT EXISTS "OffreEmploi_Langue" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "langue_id" INT REFERENCES "Langue"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "langue_id")
);

CREATE TABLE IF NOT EXISTS "OffreEmploi_Competence" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "competence_id" INT REFERENCES "Competence"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "competence_id")
);
