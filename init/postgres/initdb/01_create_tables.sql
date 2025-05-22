-- TABLES DE RÉFÉRENCE
CREATE TABLE IF NOT EXISTS "Entreprise" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "Ville" (
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

CREATE TABLE IF NOT EXISTS "TypeContrat" (
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
  "jobId" VARCHAR(255) UNIQUE,
  "dateCreation" DATE DEFAULT CURRENT_DATE,
  "libelle" VARCHAR(255),
  "experience_id" INT REFERENCES "Experience"("id") ON DELETE SET NULL,
  "duree_travail_id" INT REFERENCES "DureeTravail"("id") ON DELETE SET NULL,
  "entreprise_id" INT REFERENCES "Entreprise"("id") ON DELETE SET NULL,
  "ville_id" INT REFERENCES "Ville"("id") ON DELETE SET NULL,
  "salaire_id" INT REFERENCES "Salaire"("id") ON DELETE SET NULL,
  "mode_travail_id" INT REFERENCES "ModeTravail"("id") ON DELETE SET NULL,
  "type_contrat_id" INT REFERENCES "TypeContrat"("id") ON DELETE SET NULL,
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

-- Ajout de contraintes supplémentaires

-- Vérifier si la contrainte existe déjà
DO $$
BEGIN
    -- Vérifier si la contrainte d'unicité existe déjà sur jobId
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'offreemploi_jobid_key'
    ) THEN
        -- Ajouter la contrainte si elle n'existe pas
        ALTER TABLE "OffreEmploi" ADD CONSTRAINT "offreemploi_entreprise_libelle_key" UNIQUE ("entreprise_id", "libelle");
    END IF;
END $$;

-- Ajouter un index pour améliorer les performances de recherche sur jobId
CREATE INDEX IF NOT EXISTS "idx_offreemploi_jobid" ON "OffreEmploi" ("jobId");

-- Ajout de contraintes d'unicité sur le libellé pour les tables de référence

-- Entreprise
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'entreprise_libelle_key'
    ) THEN
        ALTER TABLE "Entreprise" ADD CONSTRAINT "entreprise_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Ville
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'ville_libelle_key'
    ) THEN
        ALTER TABLE "Ville" ADD CONSTRAINT "ville_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Salaire
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'salaire_libelle_key'
    ) THEN
        ALTER TABLE "Salaire" ADD CONSTRAINT "salaire_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Formation
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'formation_libelle_key'
    ) THEN
        ALTER TABLE "Formation" ADD CONSTRAINT "formation_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Compétence
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'competence_libelle_key'
    ) THEN
        ALTER TABLE "Competence" ADD CONSTRAINT "competence_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Experience
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'experience_libelle_key'
    ) THEN
        ALTER TABLE "Experience" ADD CONSTRAINT "experience_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- DureeTravail
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'dureetravail_libelle_key'
    ) THEN
        ALTER TABLE "DureeTravail" ADD CONSTRAINT "dureetravail_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Source
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'source_libelle_key'
    ) THEN
        ALTER TABLE "Source" ADD CONSTRAINT "source_libelle_key" UNIQUE ("libelle");
    END IF;
END $$;

-- Ajout d'index sur les tables de jointure pour améliorer les performances

-- Index pour OffreEmploi_Formation
CREATE INDEX IF NOT EXISTS "idx_offreemploi_formation_offre_id" ON "OffreEmploi_Formation" ("offre_id");
CREATE INDEX IF NOT EXISTS "idx_offreemploi_formation_formation_id" ON "OffreEmploi_Formation" ("formation_id");

-- Index pour OffreEmploi_Langue
CREATE INDEX IF NOT EXISTS "idx_offreemploi_langue_offre_id" ON "OffreEmploi_Langue" ("offre_id");
CREATE INDEX IF NOT EXISTS "idx_offreemploi_langue_langue_id" ON "OffreEmploi_Langue" ("langue_id");

-- Index pour OffreEmploi_Competence
CREATE INDEX IF NOT EXISTS "idx_offreemploi_competence_offre_id" ON "OffreEmploi_Competence" ("offre_id");
CREATE INDEX IF NOT EXISTS "idx_offreemploi_competence_competence_id" ON "OffreEmploi_Competence" ("competence_id");
