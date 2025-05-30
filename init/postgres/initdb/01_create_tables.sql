-- TABLES DE RÉFÉRENCE
CREATE TABLE IF NOT EXISTS "Entreprise" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "Ville" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "Competence" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(255),
    "categorie" VARCHAR(255)
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

CREATE TABLE IF NOT EXISTS "CompetenceDateAgg" (
    "id" SERIAL PRIMARY KEY,
    "competence_id" INT REFERENCES "Competence" ("id") ON DELETE CASCADE,
    "date" DATE NOT NULL,
    "count" INT NOT NULL DEFAULT 0,
    UNIQUE ("competence_id", "date")
);

-- Buffer pour l'agrégation des compétences par date
CREATE TABLE IF NOT EXISTS "CompetenceDateBuffer" (
    "id" SERIAL PRIMARY KEY,
    "competence_id" INT NOT NULL,
    "date" DATE NOT NULL
);

-- Mapping entre les libellés et les types de contrat
CREATE TABLE IF NOT EXISTS "MappingTypeContrat" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(100) UNIQUE NOT NULL,
    "type_contrat_id" INTEGER REFERENCES "TypeContrat" (id) ON DELETE CASCADE
);

-- Mapping entre les libellés et les modes de travail
CREATE TABLE IF NOT EXISTS "MappingModeTravail" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(100) UNIQUE NOT NULL,
    "mode_travail_id" INTEGER REFERENCES "ModeTravail" (id) ON DELETE CASCADE
);

-- Mapping entre les libellés et les durées de travail
CREATE TABLE IF NOT EXISTS "MappingDureeTravail" (
    "id" SERIAL PRIMARY KEY,
    "libelle" VARCHAR(100) UNIQUE NOT NULL,
    "duree_travail_id" INTEGER REFERENCES "DureeTravail" (id) ON DELETE CASCADE
);

-- Mapping entre les libellés et les compétences
CREATE TABLE IF NOT EXISTS "MappingCompetence" (
    id SERIAL PRIMARY KEY,
    libelle VARCHAR(100) UNIQUE NOT NULL, -- mot brut trouvé
    competence_id INTEGER REFERENCES "Competence" (id) ON DELETE CASCADE
);

-- TABLE PRINCIPALE
CREATE TABLE IF NOT EXISTS "OffreEmploi" (
    "id" SERIAL PRIMARY KEY,
    "jobId" VARCHAR(255) UNIQUE,
    "url" VARCHAR(255) UNIQUE,
    "dateCreation" DATE DEFAULT CURRENT_DATE,
    "libelle" VARCHAR(255),
    "duree_travail_id" INT REFERENCES "DureeTravail" ("id") ON DELETE SET NULL,
    "entreprise_id" INT REFERENCES "Entreprise" ("id") ON DELETE SET NULL,
    "ville_id" INT REFERENCES "Ville" ("id") ON DELETE SET NULL,
    "mode_travail_id" INT REFERENCES "ModeTravail" ("id") ON DELETE SET NULL,
    "type_contrat_id" INT REFERENCES "TypeContrat" ("id") ON DELETE SET NULL,
    "source_id" INT REFERENCES "Source" ("id") ON DELETE SET NULL
);

-- RELATIONS N:N

CREATE TABLE IF NOT EXISTS "OffreEmploi_Competence" (
    "offre_id" INT REFERENCES "OffreEmploi" ("id") ON DELETE CASCADE,
    "competence_id" INT REFERENCES "Competence" ("id") ON DELETE CASCADE,
    PRIMARY KEY ("offre_id", "competence_id")
);

-- Ajout de contraintes supplémentaires

-- Index sur jobId
CREATE INDEX IF NOT EXISTS "idx_offreemploi_jobid" ON "OffreEmploi" ("jobId");

-- Contraintes d'unicité

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

-- Competence
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

-- Index sur les tables de jointure

CREATE INDEX IF NOT EXISTS "idx_offreemploi_competence_offre_id" ON "OffreEmploi_Competence" ("offre_id");

CREATE INDEX IF NOT EXISTS "idx_offreemploi_competence_competence_id" ON "OffreEmploi_Competence" ("competence_id");