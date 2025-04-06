-- Création des tables
CREATE TABLE IF NOT EXISTS "OffreEmploi" ( 
  "id" SERIAL PRIMARY KEY,
  "source" VARCHAR,
  "source_offre_id" VARCHAR UNIQUE,
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
  "experienceCommentaire" VARCHAR,
  "dureeTravailLibelle" VARCHAR,
  "dureeTravailLibelleConverti" VARCHAR,
  "complementExercice" VARCHAR,
  "conditionExercice" VARCHAR,
  "alternance" BOOLEAN,
  "salaire_id" INT,
  "contact_id" INT,
  "agence_id" INT,
  "nombrePostes" INTEGER,
  "accessibleTH" BOOLEAN,
  "deplacementCode" VARCHAR,
  "deplacementLibelle" VARCHAR,
  "qualificationCode" VARCHAR,
  "qualificationLibelle" VARCHAR,
  "codeNAF" VARCHAR,
  "secteurActivite" VARCHAR,
  "secteurActiviteLibelle" VARCHAR,
  "trancheEffectifEtab" VARCHAR,
  "offresManqueCandidats" BOOLEAN,
  "origine_id" INT
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

CREATE TABLE IF NOT EXISTS "Formation" (
  "id" SERIAL PRIMARY KEY,
  "codeFormation" VARCHAR,
  "domaineLibelle" VARCHAR,
  "niveauLibelle" VARCHAR,
  "commentaire" TEXT,
  "exigence" VARCHAR(1) CHECK ("exigence" IN ('E', 'S'))  -- E : exigée, S : souhaitée
);

-- Table de liaison entre offre d'emploi et formation (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_Formation" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "formation_id" INT REFERENCES "Formation"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "formation_id")
);

CREATE TABLE IF NOT EXISTS "Langue" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR UNIQUE NOT NULL,
  "exigence" VARCHAR(1) CHECK ("exigence" IN ('E', 'S'))  -- E: exigée, S: souhaitée
);

-- Table de liaison entre offre d'emploi et langue (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_Langue" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "langue_id" INT REFERENCES "Langue"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "langue_id")
);

CREATE TABLE IF NOT EXISTS "Permis" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR UNIQUE NOT NULL,
  "exigence" VARCHAR(1) CHECK ("exigence" IN ('E', 'S'))  -- E: exigé, S: souhaité
);

-- Table de liaison entre offre d'emploi et permis (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_Permis" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "permis_id" INT REFERENCES "Permis"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "permis_id")
);

CREATE TABLE IF NOT EXISTS "OutilBureautique" (
  "id" SERIAL PRIMARY KEY,
  "libelle" VARCHAR UNIQUE NOT NULL
);

-- Table de liaison entre offre d'emploi et Outil Bureautique (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_OutilBureautique" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "outil_id" INT REFERENCES "OutilBureautique"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "outil_id")
);

CREATE TABLE IF NOT EXISTS "Competence" (
  "id" SERIAL PRIMARY KEY,
  "code" VARCHAR,
  "libelle" VARCHAR,
  "exigence" VARCHAR(1) CHECK ("exigence" IN ('E', 'S'))
);

-- Table de liaison entre offre d'emploi et Outil Competence (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_Competence" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "competence_id" INT REFERENCES "Competence"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "competence_id")
);

CREATE TABLE IF NOT EXISTS "Salaire" (
  "id" SERIAL PRIMARY KEY,
  "libelle" TEXT,
  "commentaire" TEXT,
  "complement1" TEXT,
  "complement2" TEXT
);

CREATE TABLE IF NOT EXISTS "Contact" (
  "id" SERIAL PRIMARY KEY,
  "nom" VARCHAR,
  "coordonnees1" TEXT,
  "coordonnees2" TEXT,
  "coordonnees3" TEXT,
  "telephone" VARCHAR,
  "courriel" VARCHAR,
  "commentaire" TEXT,
  "urlRecruteur" TEXT,
  "urlPostulation" TEXT
);

CREATE TABLE IF NOT EXISTS "Agence" (
  "id" SERIAL PRIMARY KEY,
  "telephone" VARCHAR,
  "courriel" VARCHAR
);

CREATE TABLE IF NOT EXISTS "QualiteProfessionnelle" (
  "id" SERIAL PRIMARY KEY,
  "libelle" TEXT,
  "description" TEXT
);

-- Table de liaison entre offre d'emploi et QualiteProfessionnelle (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_QualiteProfessionnelle" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "qualite_id" INT REFERENCES "QualiteProfessionnelle"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "qualite_id")
);

CREATE TABLE IF NOT EXISTS "OrigineOffre" (
  "id" SERIAL PRIMARY KEY,
  "origine" VARCHAR,
  "urlOrigine" TEXT
);

CREATE TABLE IF NOT EXISTS "Partenaire" (
  "id" SERIAL PRIMARY KEY,
  "nom" TEXT,
  "url" TEXT UNIQUE,
  "logo" TEXT
);

CREATE TABLE IF NOT EXISTS "OrigineOffre_Partenaire" (
  "origine_id" INT REFERENCES "OrigineOffre"("id") ON DELETE CASCADE,
  "partenaire_id" INT REFERENCES "Partenaire"("id") ON DELETE CASCADE,
  PRIMARY KEY ("origine_id", "partenaire_id")
);

CREATE TABLE IF NOT EXISTS "ContexteTravail" (
  "id" SERIAL PRIMARY KEY,
  "libelle" TEXT UNIQUE NOT NULL,
  "type" VARCHAR CHECK (type IN ('horaire', 'condition'))
);

-- Table de liaison entre offre d'emploi et ContexteTravail (relation N:N)
CREATE TABLE IF NOT EXISTS "OffreEmploi_ContexteTravail" (
  "offre_id" INT REFERENCES "OffreEmploi"("id") ON DELETE CASCADE,
  "contexte_id" INT REFERENCES "ContexteTravail"("id") ON DELETE CASCADE,
  PRIMARY KEY ("offre_id", "contexte_id")
);